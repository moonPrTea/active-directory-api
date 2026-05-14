from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from dao import create_new_employee
from functions import check_headers
from serializers import Employee, ErrorResponse

router = APIRouter(prefix="/employee")

@router.post("", response_model=Employee)
def create_employee(employee: Employee, request: Request):
    if not check_headers(request.headers):
        error_response = ErrorResponse(status="BAD_REQUEST", message="Authorization error")

        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump()
        )

    operation_status = create_new_employee(employee)
    if operation_status != "User created successfully":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=operation_status
        )

    return JSONResponse({
        "message": operation_status
    })
