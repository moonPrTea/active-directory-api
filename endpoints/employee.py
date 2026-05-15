from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from dao import create_new_employee
from serializers import Employee, ResponseStatus

router = APIRouter(prefix="/employee")

@router.post("", response_model=Employee)
async def create_employee(employee: Employee):
    operation_status = create_new_employee(employee)
    if operation_status != ResponseStatus.CREATED_WITH_PASSWORD:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=operation_status
        )

    return JSONResponse({
        "message": operation_status
    })
