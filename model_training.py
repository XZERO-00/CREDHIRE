"""
model_training.py (Updated for single skill input)
- CT marks out of 30 (auto-converted to percentage)
- Single skill input that applies to all semesters
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

DATA_FILE = "StudentData.xlsx"
OUT_DATA_AUTOGEN = "StudentData_autogen.xlsx"
MODEL_FILE = "job_model.pkl"

def prepare_extended_dataframe(df):
    rng = np.random.RandomState(42)
    
    # Determine base score
    if "Total_Score" in df.columns:
        base = df["Total_Score"].astype(float).fillna(df["Total_Score"].mean())
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 0:
            base = df[numeric_cols].mean(axis=1).fillna(70.0)
        else:
            base = pd.Series(70.0, index=df.index)

    # Scale base to 40-100
    minb, maxb = base.min(), base.max()
    if maxb - minb > 0:
        base_scaled = 40 + 60 * (base - minb) / (maxb - minb)
    else:
        base_scaled = pd.Series(70.0, index=base.index)

    ext = pd.DataFrame(index=df.index)

    # Process skills (single entry)
    if "Skills" in df.columns:
        skill_counts = df["Skills"].str.split(',').str.len().fillna(0) * 10
    else:
        skill_counts = pd.Series(5, index=df.index)  # Default if no skills

    for s in range(1, 9):
        # CT marks (out of 30 converted to percentage)
        ct1_col = f"CT1_Sem{s}"
        ct2_col = f"CT2_Sem{s}"
        
        if ct1_col in df.columns:
            ext[ct1_col] = (df[ct1_col].astype(float) / 30 * 100).clip(0, 100)
        else:
            noise_ct1 = rng.normal(0, 6, size=len(base_scaled))
            ext[ct1_col] = np.clip(base_scaled + noise_ct1, 0, 100).round(2)
        
        if ct2_col in df.columns:
            ext[ct2_col] = (df[ct2_col].astype(float) / 30 * 100).clip(0, 100)
        else:
            noise_ct2 = rng.normal(0, 6, size=len(base_scaled))
            ext[ct2_col] = np.clip(base_scaled + noise_ct2, 0, 100).round(2)
        
        # Final exam (out of 100)
        final_col = f"Final_Sem{s}"
        if final_col in df.columns:
            ext[final_col] = df[final_col].astype(float).clip(0, 100)
        else:
            noise_final = rng.normal(0, 8, size=len(base_scaled))
            ext[final_col] = np.clip(base_scaled + noise_final + 2, 0, 100).round(2)
        
        # Same skill count for all semesters
        ext[f"Skill_Sem{s}"] = skill_counts

    # Target variable
    if "Placed" in df.columns:
        ext["Placed"] = df["Placed"].astype(int)
    else:
        final_avg = ext[[f"Final_Sem{s}" for s in range(1, 9)]].mean(axis=1)
        skill_avg = ext[[f"Skill_Sem{s}" for s in range(1, 9)]].mean(axis=1)
        score = (0.7 * (final_avg / 100.0)) + (0.3 * (skill_avg / 100.0))
        ext["Placed"] = (score > 0.5).astype(int)

    return ext

def train_full_model():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Place {DATA_FILE} in project root and re-run.")

    print("Loading", DATA_FILE)
    df = pd.read_excel(DATA_FILE)
    ext = prepare_extended_dataframe(df)
    ext.to_excel(OUT_DATA_AUTOGEN, index=False)
    print("Saved auto-generated dataset to:", OUT_DATA_AUTOGEN)

    # Features (24 CT/Final + 8 Skill)
    features = []
    for s in range(1, 9):
        features.extend([f"CT1_Sem{s}", f"CT2_Sem{s}", f"Final_Sem{s}", f"Skill_Sem{s}"])

    X = ext[features]
    y = ext["Placed"].astype(int)

    print("Training RandomForest...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    joblib.dump({"model": clf, "features": features}, MODEL_FILE)
    print("Saved model to:", MODEL_FILE)

if __name__ == "__main__":
    train_full_model()