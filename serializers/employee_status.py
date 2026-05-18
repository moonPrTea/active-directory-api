from enum import Enum

class EmployeeStatus(str, Enum):
    USER_ALREADY_EXISTS = "User already exists in other container"
    UNUNIQUE_USER_PRINCIPAL_NAME = "User with current userPrincipalName already exists"
    NOT_FOUND = "User with current identificator doesn't exist"
    CREATED_WITH_PASSWORD = "User and its password saved successfully"
