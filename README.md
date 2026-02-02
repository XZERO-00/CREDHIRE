# 🎯 CREDHIRE  
### 🚀 AI-Powered Job Placement Prediction System for Diploma Students

**CREDHIRE** is an intelligent web application that predicts the **job placement probability** of diploma students using **Machine Learning**.  
It analyzes **academic performance** and **skill sets** to provide early insights — allowing students to improve *before* placement interviews.

> 🎓 For **Students** | 🏫 **Colleges** | 👨‍🏫 **Career Counselors**

---

## 🌟 Why CREDHIRE?

- ✅ Early placement readiness evaluation  
- 🤖 AI-driven predictions (not guesswork)  
- 📊 Clear confidence score  
- 📱 Clean & mobile-friendly interface  

---

## 🧠 How It Works

### 1️⃣ Input
- Class Test (CT) marks *(out of 30)*  
- Final exam marks *(out of 100)*  
- Skills *(comma-separated)*  

Example:
Java, Python, Communication
---

### 2️⃣ AI Processing
- Converts CT marks → percentage  
- Encodes skills numerically  
- Applies Random Forest ML model  

---

### 3️⃣ Output
- ✅ Placed / ❌ Not Placed  
- 📈 Confidence percentage  
- 📂 Automatically saved in history  

---

## 📌 Example

**Input**
- CT Scores: `28, 26, 27, 29`
- Final Exam Marks: `85, 78, 92`
- Skills: `Python, Teamwork`

**Output**
---

## 🎯 Objectives

- 🎓 Help **students** assess placement readiness  
- 🏫 Assist **colleges** in identifying at-risk students  
- 👨‍🏫 Support **career counselors** with data-driven guidance  

---

## 🛠️ Technologies Used

### 🔙 Backend
- Python 3.8+
- Flask
- SQLite
- SQLAlchemy
- scikit-learn
- Pandas & NumPy

---

### 🎨 Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Responsive Design

---

### 🤖 Machine Learning
- Random Forest Classifier  
- 200 estimators  
- 32 engineered features  
- Skill text processing  
- Automatic CT score normalization  

---

## ✨ Key Features

### 📊 Prediction System
- Supports **8 semesters**
- Auto CT score conversion
- Single skill input
- Placement probability + confidence

---

### 👤 User Management
- Secure login & registration
- User profile
- Prediction history

---

### 📈 Data Handling
- Excel (`StudentData.xlsx`) support
- Missing data handling
- Model retraining capability

---

### 🎨 User Experience
- Minimal input forms
- Clean dashboard UI
- Mobile + desktop support
- Detailed result breakdown

---

### 🔧 Technical Highlights
- SQLite persistent database
- Joblib ML model (`job_model.pkl`)
- RESTful API endpoints

---

## 🔄 Example Workflow

1. **User Enters**
   - CT marks (out of 30)
   - Final exam marks
   - Skills (once)

2. **System Processes**
   - Normalizes marks
   - Encodes skills
   - Runs ML model

3. **Result**
   - Placed / Not Placed
   - Confidence percentage
   - Stored in database

---

## 🚀 Installation & Setup

```bash
# Clone repository
git clone https://github.com/your-username/CREDHIRE.git
cd CREDHIRE

# Create virtual environment
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

📂 Project Structure
Copy code
Text
CREDHIRE/
│
├── app.py                # Main Flask app
├── static/               # CSS, JS, assets
├── templates/            # HTML templates
├── models/               # ML model & preprocessing
├── database.db           # SQLite database
├── requirements.txt      # Dependencies
└── README.md             # Documentation

🔮 Future Enhancements
📊 Performance analytics dashboards
🧠 Deep learning integration
🎯 Personalized improvement suggestions
☁ Cloud deployment

⭐ Conclusion
CREDHIRE bridges the gap between education and employability using AI — empowering students with clarity and confidence.

---

If you want:
- GitHub **badges**
- **Dark / neon theme README**
- College **project report format**
- **Landing page HTML**

Just say the word.