from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from Tool import Tool
from Main import ReservationManager, ComplaintManager, ToolManager

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used to manage user sessions

# Initialize managers
user_manager = {}
reservation_manager = ReservationManager()
complaint_manager = ComplaintManager()
tool_manager = ToolManager(admin_password="admin123")  # Set admin password

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if username in user_manager:
            return "User already exists!"
        user_manager[username] = User(username, password, email)
        return redirect(url_for("login"))
    return render_template("register.html")

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_manager.get(username)
        if user and user.password_hash == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "Invalid login details"
    return render_template("login.html")

# Dashboard for logged-in users
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["user"])

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
