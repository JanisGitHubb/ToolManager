from datetime import datetime
from Python.User import User


class ComplaintError(Exception):
    """Custom exception for complaint errors."""
    pass
class Complaint:
    def __init__(self, complaint_id, complaining_user, reported_user, complaint_text):
        self.complaint_id = complaint_id
        self.complaining_user = complaining_user
        self.reported_user = reported_user
        self.complaint_text = complaint_text
        self.created_at = datetime.now()


    @classmethod
    def create_complaint(cls, complaint_id, complaining_user, reported_user, complaint_text):
        """Validates input and only creates a Complaint object if valid."""

        print(f"DEBUG: Creating complaint ID={complaint_id}, From={complaining_user}, Against={reported_user}")

        if complaining_user == reported_user:
            raise ComplaintError("❌ Error: A user cannot file a complaint against themselves.")

        if not cls.user_exists(reported_user):
            raise ComplaintError("❌ Error: Reported user does not exist!")

        if not complaint_text.strip():
            raise ComplaintError("❌ Error: Complaint text cannot be empty!")

        print("DEBUG: ✅ Complaint successfully created!")
        return cls(complaint_id, complaining_user, reported_user, complaint_text)

    def user_exists(username):
        existing_users = ["Alice", "Bob", "Charlie"]  # Replace with actual user validation
        return username in existing_users