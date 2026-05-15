import enum

class ResponseStatus(str, enum.Enum):
    INVALID_PAYLOAD = ""
    USER_ALREADY_EXISTS = "User already exists in other container"
    UNUNIQUE_USER_PRINCIPAL_NAME = "User with current userPrincipalName already exists"
    UNKNOWN_ERROR = "Something went wrong. Try again"
    OPERATION_PERFORMED = "User created successfully"
    CREATED_WITH_PASSWORD = "User and its password saved successfully"
