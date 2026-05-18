from ldap3 import SUBTREE, MODIFY_ADD, MODIFY_DELETE

from dao.employee import get_employee_record
from dependencies import ldap
from settings import settings
from serializers import EmployeeGroup, ResponseStatus, EmployeeAndGroup, GroupStatus, EmployeeStatus


def create_group(group: EmployeeGroup) -> GroupStatus | ResponseStatus:
    if check_group_exists(group.group):
        return GroupStatus.GROUP_ALREADY_EXISTS

    group_dn = f"cn={group.group},ou={settings.ldap.GROUP_OU},{settings.ldap.BASE_DN}"
    group_attrs = add_group_attrs(group)

    ldap.add(group_dn, object_class=['top', 'group'], attributes=group_attrs)
    return check_operation_result(ldap.result.get("result"))


def add_group_member(employee_group: EmployeeAndGroup):
    group_record = check_group_exists(employee_group.group)
    if not group_record:
        return GroupStatus.NOT_FOUND_GROUP

    employee_record = get_employee_record(employee_group.user_principal_name, "userPrincipalName")
    if not employee_record:
        return EmployeeStatus.NOT_FOUND

    employee_dn = employee_record[0].entry_dn
    group_dn = group_record[0].entry_dn

    ldap.modify(group_dn, {'member': [(MODIFY_ADD, [employee_dn])]})
    return check_operation_result(ldap.result.get("result"))


def delete_group_member(employee_group: EmployeeAndGroup):
    group_record = check_group_exists(employee_group.group)
    if not group_record:
        return GroupStatus.NOT_FOUND_GROUP

    employee_record = get_employee_record(employee_group.user_principal_name, "userPrincipalName")
    if not employee_record:
        return EmployeeStatus.NOT_FOUND

    employee_dn = employee_record[0].entry_dn
    group_dn = group_record[0].entry_dn

    ldap.modify(group_dn, {'member': [(MODIFY_DELETE, [employee_dn])]})
    return check_operation_result(ldap.result.get("result"))


def group_members(group: str):
    group_record = check_group_exists(group)
    if not group_record:
        return GroupStatus.NOT_FOUND_GROUP, None

    group_dn = group_record[0]

    if not 'member' in group_dn:
        return GroupStatus.NO_MEMBERS_IN_GROUP, None

    return None, group_dn.member.values



def check_group_exists(group_name: str):
    group_filter = f'(cn={group_name})'
    ldap.search(settings.ldap.BASE_DN, group_filter, search_scope=SUBTREE, attributes=['*'])

    return ldap.entries


def add_group_attrs(group: EmployeeGroup):
    group_attrs = {
        'cn': group.group,
        'sAMAccountName': group.group,
        'description': group.description
    }

    return group_attrs


def check_operation_result(result_code: int) -> GroupStatus | ResponseStatus:
    match result_code:
        case 68:
            return GroupStatus.GROUP_ALREADY_EXISTS
        case 0:
            return ResponseStatus.OPERATION_PERFORMED
        case _:
            return ResponseStatus.UNKNOWN_ERROR
