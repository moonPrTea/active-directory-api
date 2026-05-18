import enum

class ResponseStatus(str, enum.Enum):
    INVALID_PAYLOAD = "Invalid payload for route"
    UNKNOWN_ERROR = "Something went wrong. Try again"
    OPERATION_PERFORMED = "Operation performed successfully"
