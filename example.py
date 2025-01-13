from abc import ABC, abstractmethod  # For abstraction

class Tool(ABC):  # Abstract base class
    def __init__(self, name, available=True):
        self._name = name
        self._available = available

    @abstractmethod
    def reserve(self, user):
        pass

    def check_availability(self):
        return self._available


class Microwave(Tool):  # Example of inheritance
    def __init__(self, name, power, available=True):
        super().__init__(name, available)
        self._power = power

    def reserve(self, user):
        if self._available:
            self._available = False
            print(f"Microwave {self._name} reserved by {user}")
        else:
            print(f"Microwave {self._name} is already in use.")


class CoffeeMachine(Tool):  # Example of polymorphism
    def __init__(self, name, coffee_type, available=True):
        super().__init__(name, available)
        self._coffee_type = coffee_type

    def reserve(self, user):
        if self._available:
            self._available = False
            print(f"Coffee Machine {self._name} reserved by {user}")
        else:
            print(f"Coffee Machine {self._name} is already in use.")


class User:
    def __init__(self, username):
        self._username = username

    def make_reservation(self, tool):
        tool.reserve(self._username)
