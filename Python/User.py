class User:
    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.__email = email  # Encapsulated email (private attribute)

    # Getter for email
    @property
    def email(self):
        return self.__email

    # Setter for email (if you need to modify it)
    @email.setter
    def email(self, new_email):
        self.__email = new_email

    def __str__(self):
        return f"User: {self.username}, Email: {self.email}"  # Uses the getter
