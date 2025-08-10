import os
import numpy as np
import joblib

MODEL_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "job_model.pkl")

def load_model():
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(f"Model file not found: {MODEL_FILE}")
    data = joblib.load(MODEL_FILE)
    return data["model"], data["features"]

def process_skills(skill_text):
    """Count skills from single text input"""
    if not skill_text or str(skill_text).lower().strip() in ["none", "na", ""]:
        return 0
    return len([s.strip() for s in skill_text.split(',') if s.strip()]) * 10

def predict_from_inputs(ct1_scores, ct2_scores, final_scores, skill_text):
    model, features = load_model()
    
    # Convert CT scores from /30 to percentage
    ct1_percent = np.array(ct1_scores) / 30 * 100
    ct2_percent = np.array(ct2_scores) / 30 * 100
    
    # Process single skill text
    skill_count = process_skills(skill_text)
    
    # Prepare input array (same skill count for all semesters)
    X = []
    for s in range(8):  # 8 semesters
        X.extend([
            ct1_percent[s], 
            ct2_percent[s], 
            final_scores[s], 
            skill_count  # Same count for all semesters
        ])
    
    arr = np.array(X).reshape(1, -1)
    proba = model.predict_proba(arr)[0]
    label = int(model.predict(arr)[0])
    return {
        "label": label,
        "probability": float(proba[label]),
        "probs": proba.tolist(),
        "skill_count": skill_count
    }