from fastapi import APIRouter

from dao import create_group
from serializers import EmployeeGroup

router = APIRouter(prefix="/employee_group")

@router.post("")
async def create_employee_group(employee_group: EmployeeGroup):
    response_status = create_group(employee_group)

    return {
        "status": response_status
    }


