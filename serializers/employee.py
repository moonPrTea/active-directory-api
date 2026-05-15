from pydantic import BaseModel

class Employee(BaseModel):
    first_name: str
    second_name: str
    middle_name: str | None = None
    sAMAccountName: str
    userPrincipalName: str
    password: str
    email: str
