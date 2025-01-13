from Tool import *
from User import *
from Complaint import *
from Reservations import *

def main():
    # Tool
    tool1 = Tool("Maizisu panna", "Apraksts", available=True)
    tool2 = Tool("Mikrovilnu krasns", "Apraksts", available=True)

    # Users
    user1 = User("Janis", "1234", "janis@example.com")
    user2 = User("Peteris", "5678", "peteris@example.com")

    # Vienas pers. Reservation
    single_reservation = SingleReservation(tool1.tool_name, "2024-12-05 10:00", "2024-12-05 12:00", user1.username)
    tool1.mark_as_reserved()  # Update tool availability

    # Vairaku Reservation
    multiple_reservation = MultipleReservation(tool2.tool_name, "2024-12-06 14:00", "2024-12-06 16:00", 
                                               [user1.username, user2.username])

    # Complaint
    complaint = Complaint(1, user2.username, user1.username, "The tool was not returned on time.")

    # Print all objects
    print(tool1)
    print(user1)
    print(user1.email)
    print(single_reservation)
    print(multiple_reservation)
    print(complaint)

if __name__ == "__main__":
    main()
