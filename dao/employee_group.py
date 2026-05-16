from ldap3 import SUBTREE

from dependencies import ldap
from settings import settings
from serializers import EmployeeGroup, ResponseStatus


def create_group(group: EmployeeGroup) -> ResponseStatus:
    if check_group_exists(group.group): return ResponseStatus.NOT_FOUND_GROUP

    group_dn = f"cn={group.group},ou={settings.ldap.GROUP_OU},{settings.ldap.BASE_DN}"
    group_attrs = add_group_attrs(group)

    ldap.add(group_dn, object_class=['top', 'group'], attributes=group_attrs)
    return check_operation_result(ldap.result.get("result"))


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


def check_operation_result(result_code: int) -> ResponseStatus:
    match result_code:
        case 68:
            return ResponseStatus.GROUP_ALREADY_EXISTS
        case 0:
            return ResponseStatus.OPERATION_PERFORMED
        case _:
            return ResponseStatus.UNKNOWN_ERROR
