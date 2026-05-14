from pydantic import BaseModel

class Employee(BaseModel):
    first_name: str
    second_name: str
    middle_name: str
    sAMAccountName: str
    userPrincipalName: str
    password: str
    email: str
