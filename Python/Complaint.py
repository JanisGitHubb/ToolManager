from datetime import datetime

class Complaint:
    def __init__(self, complaint_id, complaining_user, reported_user, complaint_text):
        self.complaint_id = complaint_id
        self.complaining_user = complaining_user
        self.reported_user = reported_user
        self.complaint_text = complaint_text
        self.created_at = datetime.now()

    def __str__(self):
        return (f"Complaint ID: {self.complaint_id}, Complaining User: {self.complaining_user}, "
                f"Reported User: {self.reported_user}, Text: {self.complaint_text}, Created At: {self.created_at}")
