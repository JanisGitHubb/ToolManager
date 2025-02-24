from abc import ABC, abstractmethod
from datetime import datetime

# Reservation base class
class Reservation(ABC):
    def __init__(self, tool_name, start_time, end_time):
        self.tool_name = tool_name
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = datetime.now()

    @abstractmethod
    def __str__(self):
        """Abstract method to enforce string representation in subclasses."""
        pass

# Single person res 
class SingleReservation(Reservation):
    def __init__(self, tool_name, start_time, end_time, user):
        super().__init__(tool_name, start_time, end_time)
        self.user = user  

    def __str__(self):
        return (f"Vienas personas rezervacija: {self.user}, Tool: {self.tool_name}, "
                f"Start: {self.start_time}, End: {self.end_time}, izveidots: {self.created_at}")

# Multiple person res (not yet integrated in html)
class MultipleReservation(Reservation):
    def __init__(self, tool_name, start_time, end_time, users):
        super().__init__(tool_name, start_time, end_time)
        self.users = users  

    def __str__(self):
        user_list = ", ".join(self.users)
        return (f"Vairaku personu rezervacija: [{user_list}], Tool: {self.tool_name}, "
                f"Start: {self.start_time}, End: {self.end_time}, Izveidots: {self.created_at}")
