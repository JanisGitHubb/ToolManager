class Tool:
    def __init__(self, tool_name, description, available=True):
        self.tool_name = tool_name
        self.description = description
        self.available = available

    def mark_as_reserved(self):
        self.available = False

    def mark_as_available(self):
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Not Available"
        return f"Tool: {self.tool_name}, Status: {status}, Description: {self.description}"
