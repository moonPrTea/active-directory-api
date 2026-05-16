from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from dao import create_new_employee, update_employee_record, deactivate_employee_account, activate_employee_account, \
    update_employee_username
from serializers import Employee, ResponseStatus, UpdateEmployee, UpdateUsername

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

@router.patch("")
async def update_employee(employee_attrs: UpdateEmployee):
    response_status = update_employee_record(employee_attrs)
    if response_status == ResponseStatus.NOT_FOUND_USER:
        raise HTTPException(
            status_code=404,
            detail={"status": response_status}
        )

    if response_status != ResponseStatus.OPERATION_PERFORMED:
        raise HTTPException(
            status_code=502,
            detail={"status": response_status}
        )

    return {
        "status": response_status
    }

@router.patch("/activate/{user_principal_name}")
async def activate_employee_record(user_principal_name: str):
    response_status = activate_employee_account(user_principal_name)
    if response_status == ResponseStatus.NOT_FOUND_USER:
        raise HTTPException(
            status_code=404,
            detail={"status": response_status}
        )

    return {
        "status": response_status
    }


@router.patch("/deactivate/{user_principal_name}")
async def activate_employee_record(user_principal_name: str):
    response_status = deactivate_employee_account(user_principal_name)
    if response_status == ResponseStatus.NOT_FOUND_USER:
        raise HTTPException(
            status_code=404,
            detail={"status": response_status}
        )

    return {
        "status": response_status
    }


@router.patch("/user_principal_name")
async def update_username(update_username: UpdateUsername):
    response_status = update_employee_username(update_username)
    if response_status == ResponseStatus.NOT_FOUND_USER:
        raise HTTPException(
            status_code=404,
            detail={"status": response_status}
        )

    return {
        "status": response_status
    }

