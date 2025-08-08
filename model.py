# 1. Importing Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt



#  Load Dataset
df = pd.read_excel(r"E:\Projects\CREDHIRE\data\StudentData.xlsx")
print(df.head())

# Data Preprocessing

#  Handling Missing Values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Encoding Categorical Columns (if any)
# df = pd.get_dummies(df, drop_first=True)

# 3.3 Fixing Outliers using IQR
for col in df.select_dtypes(include='number').columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = np.where(df[col] < lower, lower, df[col])
    df[col] = np.where(df[col] > upper, upper, df[col])

# 4. Feature Scaling
scaler = StandardScaler()
X = df.drop('Grade', axis=1)
y = df['Grade']
X_scaled = scaler.fit_transform(X)

# 5. Model Building
model = RandomForestClassifier()


# 6. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# 7. Prediction & Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Optional: Confusion matrix heatmap
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()












# Student_ID	
# First_Name	
# Last_Name
# Email
# Gender
# Age
# Department
# Attendance (%)
# Midterm_Score
# Final_Score
# Assignments_Avg
# Quizzes_Avg
# Participation_Score
# Projects_Score
# Total_Score
# Grade
# Study_Hours_per_Week
# Extracurricular_Activities
# Internet_Access_at_Home
# Parent_Education_Level
# Family_Income_Level
# Stress_Level (1-10)
# Sleep_Hours_per_Night

