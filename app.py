from flask import Flask, render_template, request, redirect, url_for, session
from Python.User import User
from Python.Tool import Tool
from Python.Main import ReservationManager, ComplaintManager, ToolManager

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

# View Tools
@app.route("/tools")
def tools():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("tools.html", tools=tool_manager.tools.values())

# Manage Reservations
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        tool_name = request.form["tool_name"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        username = session["user"]
        reservation_manager.reserve_tool(tool_name, username, start_time, end_time)

    return render_template("reservations.html", reservations=reservation_manager.reservations)

# File a Complaint
@app.route("/complaints", methods=["GET", "POST"])
def complaints():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        complaining_user = session["user"]
        reported_user = request.form["reported_user"]
        complaint_text = request.form["complaint_text"]
        complaint_manager.file_complaint(complaining_user, reported_user, "N/A", complaint_text)

    return render_template("complaints.html", complaints=complaint_manager.complaints)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
