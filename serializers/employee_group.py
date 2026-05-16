from pydantic import BaseModel


class EmployeeGroup(BaseModel):
    group: str
    description: str


class EmployeeAndGroup(BaseModel):
    group: str
    user_principal_name: str
