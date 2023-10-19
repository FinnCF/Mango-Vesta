from typing import Any

class NotInRangeError(Exception):
    """Exception raised when a value is not in the specified range."""
    
    def __init__(self, value: float, message: str = "Value not in range of 0 to 1") -> None:
        """Initialize the exception with the offending value and an optional message."""
        self.value: float = value
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        return f"NotInRangeError({self.value}, message='{self.message}')"

    def __repr__(self) -> str:
        """The official string representation of the object."""
        return self.__str__()
