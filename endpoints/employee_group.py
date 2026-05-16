from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from dao import create_group, add_group_employee
from serializers import EmployeeGroup, EmployeeAndGroup, ResponseStatus

router = APIRouter(prefix="/employee_group")

@router.post("")
async def create_employee_group(employee_group: EmployeeGroup):
    response_status = create_group(employee_group)

    return {
        "status": response_status
    }


@router.put("/move_employee")
async def move_employee_in_group(employee_group: EmployeeAndGroup):
    response_status = add_group_employee(employee_group)
    if response_status != ResponseStatus.OPERATION_PERFORMED:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=response_status
        )

    return {
        "status": response_status
    }

