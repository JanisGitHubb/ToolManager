from Python.Tool import *
from Python.User import *
from Python.Reservations import SingleReservation
from datetime import datetime, timedelta

# User Management
class UserManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password, email):
        if username in self.users:
            return "User already exists."
        self.users[username] = User(username, password, email)
        return "User registered successfully."

    def login(self, username, password):
        user = self.users.get(username)
        print(user)
        if user and user.password_hash == password:
            return f"Welcome, {username}!"
        return "Invalid username or password."

# Tool Management
class ToolManager:
    def __init__(self, admin_password):
        self.tools = {}
        self.admin_password = admin_password

    def authenticate_admin(self, password):
        return password == self.admin_password

    def add_tool(self, tool_name, description, password):

        if not self.authenticate_admin(password):
            return "Access denied: Incorrect password."
        if tool_name in self.tools:
            return "Tool already exists."
        self.tools[tool_name] = Tool(tool_name, description)
        return "Tool added successfully."

    def update_tool(self, tool_name, new_description, password):
        if not self.authenticate_admin(password):
            return "Access denied: Incorrect password."
        tool = self.tools.get(tool_name)
        if not tool:
            return "Tool not found."
        tool.description = new_description
        return "Tool updated successfully."

    def delete_tool(self, tool_name, password):
        if not self.authenticate_admin(password):
            return "Access denied: Incorrect password."
        if tool_name not in self.tools:
            return "Tool not found."
        del self.tools[tool_name]
        return "Tool deleted successfully."

    def list_tools(self):
        return [str(tool) for tool in self.tools.values()]

# Reservation System
class ReservationManager:
    def __init__(self, tool_manager):
        self.reservations = []
        self.tool_manager = tool_manager 

    def create_single_reservation(self, tool_name, start_time, end_time, user):
        # does tool exist
        if tool_name not in self.tool_manager.tools:
            return f"Error: The tool '{tool_name}' does not exist. Please select a valid tool."

        if end_time <= start_time:
            return "Error: The end time must be later than the start time."

        # is start time not in the past
        if start_time < datetime.now():
            return "Error: You cannot make a reservation for a past time."

        # Ensure start time is not more than 2 hours in advance
        max_reservation_time = datetime.now() + timedelta(hours=2)
        if start_time > max_reservation_time:
            return "Error: Reservations can only be made up to 2 hours in advance."


        # is tool available
        if not self.is_tool_available(tool_name, start_time, end_time):
            return "Tool is not available during the specified time."
        
        # create reservation, if all conditions are met
        reservation = SingleReservation(tool_name, start_time, end_time, user)
        self.reservations.append(reservation)
        return "Single reservation created successfully."

    def is_tool_available(self, tool_name, start_time, end_time):
        for reservation in self.reservations:
            if reservation.tool_name == tool_name and not (
                end_time <= reservation.start_time or start_time >= reservation.end_time
            ):
                return False
        return True

    def reservation_history(self, tool_name):
        return [str(res) for res in self.reservations if res.tool_name == tool_name]


# Example Usage in python logic (some is not included yet in html, like the admin functionality)
if __name__ == "__main__":
    admin_password = "admin123"
    tool_manager = ToolManager(admin_password)
    user_manager = UserManager()
    reservation_manager = ReservationManager()

    # User Management
    print(user_manager.register_user("alice", "password123", "alice@example.com"))
    print(user_manager.register_user("bob", "securepassword", "bob@example.com"))
    print(user_manager.login("alice", "password123"))

    # Attempting to add tools with and without the correct password
    print(tool_manager.add_tool("Microwave", "For heating food", "wrongpass"))
    print(tool_manager.add_tool("Microwave", "For heating food", "admin123"))
    print(tool_manager.add_tool("Coffee Maker", "For brewing coffee", "admin123"))
    
    # Attempting to update a tool's description
    print(tool_manager.update_tool("Microwave", "For quickly heating food", "wrongpass"))
    print(tool_manager.update_tool("Microwave", "For quickly heating food", "admin123"))
    
    # Attempting to delete a tool
    print(tool_manager.delete_tool("Coffee Maker", "wrongpass"))
    print(tool_manager.delete_tool("Coffee Maker", "admin123"))
    
    # Listing tools
    print(tool_manager.list_tools())

    # Reservation Management
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    print(reservation_manager.create_single_reservation("Microwave", start_time, end_time, "alice"))
    print(reservation_manager.reservation_history("Microwave"))


