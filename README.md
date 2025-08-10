# 🎯 CREDHIRE  
**AI-Powered Job Placement Prediction for Diploma Students**

CREDHIRE is a web application that predicts the **job placement probability** of diploma students based on their **academic performance** and **skills**.  
It’s built to help **students**, **trainers**, and **colleges** gauge placement chances early — so weak areas can be improved before actual interviews.

---

## 📌 In Simple Terms
1. **🎓 Input:**  
   Enter your class test scores (out of 30), final exam marks, and skills (e.g., `"Java, Communication"`)

2. **🤖 AI Prediction:**  
   Our trained **Random Forest ML model** analyzes your data and trends.

3. **📊 Result:**  
   Instantly see if you’re likely to get placed — with a confidence score.

4. **📂 History:**  
   All predictions are saved so you can track your progress over time.

---

## 💡 Example

**Input:**  
CT Scores: [28/30, 26/30, 27/30, ...]
Final Exam: [85, 78, 92, ...]
Skills: "Python, Teamwork"

**Output:**  
Placed (87% Confidence)


---

## 🎯 Purpose
- Give **students** a reality check on their placement readiness  
- Enable **colleges** to identify and support at-risk students  
- Assist **career counselors** in guiding candidates effectively  

---

## 🛠️ Technologies Used

### Backend:
- Python (v3.8+)
- Flask (Web framework)
- SQLite + SQLAlchemy (Database)
- scikit-learn (Random Forest Classifier)
- Pandas (Data Processing)

### Frontend:
- HTML5 / CSS3
- Vanilla JavaScript
- Responsive Design (Mobile + Desktop)

### Machine Learning:
- **Random Forest** (200 estimators)
- **32 input features** (CT scores, Finals, Skills)
- Automatic CT score conversion (`/30 → %`)
- Text-based skill processing

---

## ✨ Key Features

### 📊 Prediction System
- Accepts **8 semesters** of academic data
- Auto-converts CT scores to percentage
- Parses comma-separated skills (`"Python, Communication"`)
- Returns **placement probability + confidence score**

### 👤 User Management
- Secure **registration & login**
- Prediction **history tracking**
- User profile & settings

### 📈 Data Handling
- Excel (`StudentData.xlsx`) compatibility
- Auto feature generation for missing data
- Model retraining capability

### 🎨 User Experience
- Single-page skill input (no repetitive forms)
- Clean, mobile-friendly UI
- Detailed prediction results + skill breakdown

### 🔧 Technical Highlights
- SQLite for persistent storage
- Joblib-saved ML model (`job_model.pkl`)
- RESTful API endpoints for predictions

---

## 🚀 Example Workflow
1. **User enters:**
   - CT scores for 8 semesters (out of 30)
   - Final exam marks (out of 100)
   - Skills once (e.g., `"C++, Problem Solving"`)

2. **System processes:**
   - Converts CT scores → percentage
   - Encodes skills as numerical features
   - Runs Random Forest model

3. **Output:**
   - `Placed / Not Placed`  
   - Confidence percentage  
   - Stores result in user’s history

---

## 📦 Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/your-username/CREDHIRE.git
cd CREDHIRE

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py


📂 Project Structure
CREDHIRE/
├── app.py               # Main Flask app
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── models/              # ML model + preprocessing scripts
├── database.db          # SQLite database
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
