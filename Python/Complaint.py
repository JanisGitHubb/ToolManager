from datetime import datetime

class Complaint:
    def __init__(self, complaint_id, complaining_user, reported_user, complaint_text):
        self.complaint_id = complaint_id
        self.complaining_user = complaining_user
        self.reported_user = reported_user
        self.complaint_text = complaint_text
        self.created_at = datetime.now()

    @classmethod
    def user_exists(cls, username, user_manager):
        if username in user_manager.users:
            return True
        return False


    @classmethod
    def create_complaint(cls, complaint_id, complaining_user, reported_user, complaint_text):
        """Validates input and only creates a Complaint object if valid."""

        mock_users = ["janis","peteris", "Alice","Bob"]
          # kad būs datubāze varēs likt to, bet kamēr tās nav ir pārāk milzīgs čakars

        print(f"DEBUG: Creating complaint ID={complaint_id}, From={complaining_user}, Against={reported_user}")

        if reported_user not in mock_users:
            return "Kļūda: Lietotājs neeksistē"

        if complaining_user == reported_user:
            return "Kļūda: Lietotājs nevar sūdzēties par sevi!"

        if not complaint_text.strip():
            return "Kļūda: Sūdzības teksts nevar būt tukšs"

        print("DEBUG: Complaint successfully created!")
        return cls(complaint_id, complaining_user, reported_user, complaint_text)

class ComplaintManager:
    def __init__(self):
        self.complaints = []

    def file_complaint(self, complaining_user, reported_user, complaint_text):
        complaint_id = len(self.complaints) + 1
        result = Complaint.create_complaint(complaint_id, complaining_user, reported_user, complaint_text)

        # If the result is a string (error message), return it
        if isinstance(result, str):
            print(result)
            return result  # Return the error message to let the user know what happened

        self.complaints.append(result)  # If it's a valid complaint, append it
        print("Complaint successfully created!")
        return "Complaint filed successfully!"

    def list_complaints(self):
        return [str(complaint) for complaint in self.complaints]

