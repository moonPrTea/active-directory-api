from pydantic import BaseModel


class EmployeeGroup(BaseModel):
    group: str
    description: str
