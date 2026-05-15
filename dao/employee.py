from dependencies import ldap
from settings import settings
from serializers import Employee, ResponseStatus


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


def check_record_exist(parameter_value, parameter: str) -> bool:
    dn_address = f"{settings.ldap.BASE_DN}"
    search_url = f"({parameter}={parameter_value})"

    ldap.search(dn_address, search_url, attributes=['*'])
    if ldap.entries:
        return True
    return False


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

    if employee.middle_name is None:
        return employee_attrs

    employee_attrs['middleName'] = employee.middle_name
    return employee_attrs



