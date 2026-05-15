from ldap3 import MODIFY_REPLACE, SUBTREE

from dependencies import ldap
from settings import settings
from serializers import Employee, ResponseStatus, UpdateEmployee


def create_new_employee(employee: Employee) -> ResponseStatus:
    if check_record_exist(employee.userPrincipalName, parameter='userPrincipalName'):
        return ResponseStatus.UNUNIQUE_USER_PRINCIPAL_NAME

    fullname = " ".join(filter(None, [employee.first_name, employee.second_name, employee.middle_name]))
    entry = f'cn={fullname},ou={settings.ldap.USER_OU},{settings.ldap.BASE_DN}'
    employee_attrs = create_employee_attrs(employee, fullname)

    ldap.add(entry, attributes=employee_attrs)

    checked_result = check_operation_result(ldap.result.get("result"))
    if checked_result != ResponseStatus.OPERATION_PERFORMED:
        return checked_result

    ldap.extend.microsoft.modify_password(entry, employee.password)
    if ldap.result['description'] == 'success':
        return ResponseStatus.CREATED_WITH_PASSWORD

    return ResponseStatus.UNKNOWN_ERROR


def update_employee_record(update_employee: UpdateEmployee) -> ResponseStatus:
    employee_record = get_employee_record(update_employee.userPrincipalName, parameter='userPrincipalName')
    if employee_record is None:
        return ResponseStatus.NOT_FOUND_USER

    update_attrs = update_employee_attrs(update_employee)
    employee_dn = employee_record[0].entry_dn

    modify_items = {
        item: [(MODIFY_REPLACE, [value] if not isinstance(value, list) else value)]
        for item, value in update_attrs.items()
    }
    try:
        ldap.modify(employee_dn, modify_items)
    except Exception as e:
        return ResponseStatus.UNKNOWN_ERROR
    return ResponseStatus.OPERATION_PERFORMED


def activate_employee_account(user_principal_name: str) -> ResponseStatus:
    employee_record = get_employee_record(user_principal_name, parameter='userPrincipalName')
    if employee_record is None:
        return ResponseStatus.NOT_FOUND_USER

    employee_dn = employee_record[0].entry_dn
    ldap.modify(employee_dn, {'userAccountControl': [(MODIFY_REPLACE, 512)]})

    return ResponseStatus.OPERATION_PERFORMED


def deactivate_employee_account(user_principal_name: str) -> ResponseStatus:
    employee_record = get_employee_record(user_principal_name, parameter='userPrincipalName')
    if employee_record is None:
        return ResponseStatus.NOT_FOUND_USER

    employee_dn = employee_record[0].entry_dn
    ldap.modify(employee_dn, {'userAccountControl': [(MODIFY_REPLACE, 514)]})

    return ResponseStatus.OPERATION_PERFORMED


def check_record_exist(parameter_value, parameter: str) -> bool:
    dn_address = f"{settings.ldap.BASE_DN}"
    search_url = f"({parameter}={parameter_value})"

    ldap.search(dn_address, search_url, attributes=['*'])
    if ldap.entries:
        return True
    return False


def get_employee_record(parameter_value, parameter: str):
    dn_address = f"{settings.ldap.BASE_DN}"
    search_url = f"({parameter}={parameter_value})"

    ldap.search(dn_address, search_url, attributes=['*'])
    if ldap.entries:
        return ldap.entries
    return None


def check_operation_result(result_code: int) -> ResponseStatus:
    match result_code:
        case 68:
            return ResponseStatus.USER_ALREADY_EXISTS
        case 0:
            return ResponseStatus.OPERATION_PERFORMED
        case _:
            return ResponseStatus.UNKNOWN_ERROR


def create_employee_attrs(employee: Employee, fullname: str):
    employee_attrs = {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        'cn': fullname,
        'givenName': employee.second_name,
        'sn': employee.first_name,
        'displayName': fullname,
        'mail': employee.email,
        'UserAccountControl': 514,
        'UserPrincipalName': employee.userPrincipalName,
        'sAMAccountName': employee.sAMAccountName
    }

    if employee.middle_name is not None:
        employee_attrs['middleName'] = employee.middle_name

    return employee_attrs


def update_employee_attrs(update_employee: UpdateEmployee):
    update_attrs = {
        'mobile': update_employee.phone_number
    }

    if update_employee.department is not None:
        update_attrs['department'] = update_employee.department

    if update_employee.position is not None:
        update_attrs['title'] = update_employee.position

    return update_attrs
