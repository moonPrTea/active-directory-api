from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from dao import create_new_employee
from serializers import Employee, ResponseStatus

router = APIRouter(prefix="/employee")

@router.post("", status_code=201)
async def create_employee(employee: Employee):
    response_status = create_new_employee(employee)
    if response_status != ResponseStatus.CREATED_WITH_PASSWORD:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=response_status
        )

    return {
        "status": response_status
    }
