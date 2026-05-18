from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from dao import create_group, add_group_member, delete_group_member, group_members
from serializers import EmployeeGroup, EmployeeAndGroup, ResponseStatus, GroupStatus

router = APIRouter(prefix="/employee_group")


@router.get("/members/{group}")
async def get_group_members(group:str):
    response_status, members = group_members(group)

    if response_status is not None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=response_status
        )

    return {"members": members}

@router.post("")
async def create_employee_group(employee_group: EmployeeGroup):
    response_status = create_group(employee_group)

    return {
        "status": response_status
    }


@router.put("/add_member")
async def add_new_member(employee_group: EmployeeAndGroup):
    response_status = add_group_member(employee_group)
    if response_status != ResponseStatus.OPERATION_PERFORMED:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=response_status
        )

    return {
        "status": response_status
    }


@router.delete("/delete_member")
async def delete_new_member(employee_group: EmployeeAndGroup):
    response_status = delete_group_member(employee_group)
    if response_status != ResponseStatus.OPERATION_PERFORMED:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=response_status
        )

    return {
        "status": response_status
    }

