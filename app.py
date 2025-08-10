import os, json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from utils.db import init_db, SessionLocal, User as DBUser, History
from utils.auth import register_user, authenticate_user
from utils.predict import predict_from_inputs

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret")

# Init DB
init_db()

# Auth
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class LocalUser(UserMixin):
    def __init__(self, db_user):
        self.id = str(db_user.id)
        self.name = db_user.name
        self.email = db_user.email
        self.theme = getattr(db_user, "theme", "dark")

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    try:
        dbu = db.query(DBUser).filter(DBUser.id == int(user_id)).first()
        if dbu:
            return LocalUser(dbu)
    finally:
        db.close()
    return None

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        if not name or not email or not password:
            flash("Fill all fields.", "danger")
            return render_template("register.html")
        user, err = register_user(name, email, password)
        if err:
            flash(err, "danger")
            return render_template("register.html")
        login_user(LocalUser(user))
        flash("Registration successful. Welcome!", "success")
        return redirect(url_for("profile"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        user = authenticate_user(email, password)
        if not user:
            flash("Invalid credentials.", "danger")
            return render_template("login.html")
        login_user(LocalUser(user), remember=True)
        flash("Logged in.", "success")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/predictions", methods=["GET","POST"])
@login_required
def predictions():
    if request.method == "POST":
        try:
            # Collect inputs
            ct1_scores = [float(request.form.get(f"ct1_s{s}", 0)) for s in range(1,9)]
            ct2_scores = [float(request.form.get(f"ct2_s{s}", 0)) for s in range(1,9)]
            final_scores = [float(request.form.get(f"final_s{s}", 0)) for s in range(1,9)]
            all_skills = request.form.get("all_skills", "").strip()
            
            # Get prediction
            res = predict_from_inputs(ct1_scores, ct2_scores, final_scores, all_skills)
            label = "Placed" if res["label"] == 1 else "Not Placed"
            
            # Save history
            db = SessionLocal()
            hist = History(
                user_id=int(current_user.get_id()),
                input_data=json.dumps({
                    "ct1": ct1_scores,
                    "ct2": ct2_scores,
                    "final": final_scores,
                    "skills": all_skills,
                    "skill_count": res["skill_count"] // 10  # Store actual count
                }),
                result=label,
                probability=round(res["probability"] * 100, 2)
            )
            db.add(hist)
            db.commit()
            db.close()
            
            return render_template("predictions.html", 
                prediction=label,
                probability=round(res["probability"] * 100, 2),
                inputs={
                    "ct1": ct1_scores,
                    "ct2": ct2_scores,
                    "final": final_scores,
                    "skills": all_skills,
                    "skill_count": res["skill_count"] // 10
                })
            
        except Exception as e:
            flash(f"Prediction error: {str(e)}", "danger")
            return redirect(url_for("predictions"))
    
    return render_template("predictions.html")


@app.route("/history")
@login_required
def history():
    db = SessionLocal()
    try:
        rows = db.query(History).filter(History.user_id == int(current_user.get_id())).order_by(History.created_at.desc()).all()
    finally:
        db.close()
    return render_template("history.html", rows=rows)

@app.route("/help")
def help_page():
    faqs = [
        ("What is CREDHIRE?", "Predicts job placement using CT (out of 30), final exams, and skill counts."),
        ("How to enter skills?", "Comma-separated list (e.g., 'Java,Communication,Problem Solving')"),
        ("CT marks?", "Enter out of 30 - system auto-converts to percentage.")
    ]
    return render_template("help.html", faqs=faqs)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        flash("Message received!", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/settings", methods=["GET","POST"])
@login_required
def settings():
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.id == int(current_user.get_id())).first()
        if request.method == "POST":
            theme = request.form.get("theme","dark")
            user.theme = theme
            db.commit()
            flash("Settings saved.", "success")
            return redirect(url_for("settings"))
        return render_template("settings.html", user=user)
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)