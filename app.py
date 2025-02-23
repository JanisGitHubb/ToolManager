from flask import Flask, render_template, request, redirect, url_for, session
from Python.User import User
from Python.Tool import Tool
from Python.Main import ReservationManager, ToolManager
from Python.Complaint import ComplaintManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used to manage user sessions

# Initialize managers
user_manager = {}
complaint_manager = ComplaintManager()
tool_manager = ToolManager(admin_password="admin123")  # Set admin password
tool_manager.add_tool("Microwave", "For heating food", "admin123")
tool_manager.add_tool("Coffee Maker", "For brewing coffee", "admin123")
reservation_manager = ReservationManager(tool_manager)


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
        print(user)
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

# View & Manage Tools (Admin functionality added)
@app.route("/tools", methods=["GET", "POST"])


def tools():
    if "user" not in session:
        return redirect(url_for("login"))
    
    tool_manager.add_tool("Microwave", "For heating food", "admin123")
    tool_manager.add_tool("Coffee Maker", "For brewing coffee", "admin123")

    message = None


    if request.method == "POST":
        tool_name = request.form["tool_name"]
        description = request.form["description"]
        admin_password = request.form["admin_password"]



        if tool_manager.authenticate_admin(admin_password):
            message = tool_manager.add_tool(tool_name, description, admin_password)
        else:
            message = "Access Denied: Incorrect Admin Password"

    return render_template("tools.html", tools=list(tool_manager.tools.values()), message=message)

# Manage Reservations

@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    if "user" not in session:
        return redirect(url_for("login"))

    message = ""

    if request.method == "POST":
        tool_name = request.form["tool_name"]
        start_time = datetime.strptime(request.form["start_time"], "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(request.form["end_time"], "%Y-%m-%dT%H:%M")
        username = session["user"]
        current_time = datetime.now()

        # Check if start time is in the future
        if start_time < current_time:
            message = "Error: You cannot make a reservation for a past time."
        elif end_time <= start_time:
            message = "Error: The end time must be later than the start time."
        elif tool_name not in tool_manager.tools:
            message = f"Error: The tool '{tool_name}' does not exist. Please select a valid tool."
        else:
            # Check for overlapping reservations
            conflicting_reservation = any(
                res.tool_name == tool_name and not (end_time <= res.start_time or start_time >= res.end_time)
                for res in reservation_manager.reservations
            )

            if conflicting_reservation:
                message = f"Error: The tool '{tool_name}' is already reserved for the selected time period."
            else:
                message = reservation_manager.create_single_reservation(tool_name, start_time, end_time, username)
                
    return render_template("reservations.html", reservations=reservation_manager.reservations, message=message)

# File a Complaint
@app.route("/complaints", methods=["GET", "POST"])
def complaints():
    if "user" not in session:
        return redirect(url_for("login"))

    message = ""

    if request.method == "POST":
        complaining_user = session["user"]
        reported_user = request.form["reported_user"]
        complaint_text = request.form["complaint_text"]


        result = complaint_manager.file_complaint(complaining_user, reported_user, complaint_text)

        if isinstance(result, str):
            message = result

    return render_template("complaints.html", complaints=complaint_manager.complaints, message=message)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

