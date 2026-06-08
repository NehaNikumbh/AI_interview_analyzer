from flask import Flask, render_template, request, redirect, session, flash
import random

app = Flask(__name__)
app.secret_key = "ai_interview_secret"

users = {}

# ---------------- QUESTIONS ----------------

hr_questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?",
    "Where do you see yourself in 5 years?"
]

python_questions = [
    "What is Python?",
    "Difference between List and Tuple?",
    "What is OOP in Python?",
    "What is a Dictionary?",
    "Explain Exception Handling."
]

dbms_questions = [
    "What is DBMS?",
    "What is Primary Key?",
    "What is Foreign Key?",
    "Explain Normalization.",
    "Difference between DELETE and DROP?"
]

cloud_questions = [
    "What is Cloud Computing?",
    "What is AWS?",
    "What is Virtualization?",
    "What is SaaS?",
    "Difference between Public and Private Cloud?"
]

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if username in users:
            flash("User already exists!")
            return redirect("/register")

        users[username] = {
            "email": email,
            "password": password
        }

        flash("Registration Successful!")
        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:

            session["user"] = username
            return redirect("/dashboard")

        flash("Invalid Username or Password!")
        return redirect("/login")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"]
    )

# ---------------- INTERVIEW ----------------

@app.route("/interview/<category>")
def interview(category):

    if "user" not in session:
        return redirect("/login")

    if category == "hr":
        question = random.choice(hr_questions)

    elif category == "python":
        question = random.choice(python_questions)

    elif category == "dbms":
        question = random.choice(dbms_questions)

    elif category == "cloud":
        question = random.choice(cloud_questions)

    else:
        question = "Invalid Category"

    session["category"] = category

    return render_template(
        "interview.html",
        question=question,
        category=category
    )

# ---------------- SUBMIT ANSWER ----------------

@app.route("/next_question", methods=["POST"])
def next_question():

    if "user" not in session:
        return redirect("/login")

    answer = request.form["answer"]

    print("User Answer:", answer)

    return redirect("/result")

# ---------------- RESULT ----------------

@app.route("/result")
def result():

    if "user" not in session:
        return redirect("/login")

    score = random.randint(70, 95)

    feedback = """
    Good communication skills.
    Try adding more practical examples.
    Improve technical depth in answers.
    """

    return render_template(
        "result.html",
        score=score,
        feedback=feedback
    )

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)