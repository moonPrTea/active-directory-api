from ldap3 import MODIFY_ADD, MODIFY_DELETE, SUBTREE, MODIFY_REPLACE
from . import file_reader, ldap
from settings import ldap_settings


def check_base_dn(): #-> проверка текущего dc на существование
    if ldap.search(ldap_settings.BASE_DC, "(objectClass=*)"):
        print("текущий DN существует")
        return 'Результат пришел'
    print("текущий DN не существует")
    return False

def add_new_information(ou_name, model): #-> добавление данных в ou  
    match ou_name: 
        case "managed_accounts":
            print(model.userPrincipalName, model.fullname)
            entry = f'cn={model.fullname},ou={ldap_settings.USER_OU},{ldap_settings.BASE_DC}'
            expected_attributes = create_add_dict(model)
            
            ldap.add(entry, attributes=expected_attributes)
            print(ldap.result)
            if ldap.result['result'] == 68:
                return '17', f'пользователь есть с ид {model.identificator} в другом контейнере', ldap.result
            
            if ldap.result["result"] is True or ldap.result['result'] == 0:
                print(f"Запись {expected_attributes['cn']} добавлена")
                ldap.extend.microsoft.modify_password(entry, model.password) #-> тут попытка добавления пароля

                if ldap.result['description'] == 'success':
                    print("Пароль успешно установлен")
                    return "0", "все ок", ""
                
                print(error_handler(ldap.result['result']), 'лалала')
                return error_handler(ldap.result['result']), ldap.result['description'], ldap.result
                
            
        #-> тут код для добавления данных в managed_users
        case "managed_groups":
            result, _ = check_group_exist(model)
            if not result:
                group_adress = f"cn={model.group_name},ou={ldap_settings.GROUP_OU},{ldap_settings.BASE_DC}"
                expected_attributes = {
                    'cn': model.group_name, 
                    'sAMAccountName': model.group_name, 
                    'mail': model.group_mail, #-> необязательный атрибут
                    'name': model.group_name,
                    'description': model.description, #-> описание группы
                    'info': model.valid_name
                }
                
                ldap.add(group_adress, object_class=['top', 'group'], attributes=expected_attributes)
            
                if ldap.result['description'] == 'success':
                    return "0", "все ок"
                
                print(error_handler(ldap.result['result']))
                return error_handler(ldap.result['result']), ldap.result['description']
                    
            
            return "8", ldap.result['description'] 
 
#------> все, что связано с пользователем
def activate_employee_status(model, new_status: 512): #-> тут, активация статуса учетки
    base = f"ou={ldap_settings.BASE_DC}"
    print(base)
    
    search_filter = f"(pager={model.identificator})"
    print(model.identificator)
    print(search_filter)
    ldap.search(search_base=base, search_filter=search_filter, search_scope=SUBTREE, attributes=["pager"])

    if ldap.entries:
        current_dn = ldap.entries[0].entry_dn 
        res = check_member_of(current_dn, model)
        if res:
            print(f"Найден пользователь -- {current_dn}") #-> вывод для проверки результата
            ldap.modify(current_dn, {'userAccountControl': [(MODIFY_REPLACE, new_status)]})
            print(ldap.result)
        
            if ldap.result['description'] != "success":
                return error_handler(ldap.result['result']), ldap.result['description']
            else:
                return "0", "все ок"
            
        return "9", f"Нет доступа к изменению {model.identificator}"
    
    return "15", f"Нет пользователя: {model.identificator}"
        

def update_password(model):
    _, employee_entries = search_all_user_params(model.identificator, ldap_settings.USER_OU, "pager")
    employee_dn = employee_entries[0].entry_dn
    print(check_member_of(employee_dn, model))
    
    if check_member_of(employee_dn, model):
        ldap.extend.microsoft.modify_password(employee_dn, model.user_password) #-> тут попытка добавления пароля
        if ldap.result['description'] == 'success':
            return "0", "Пароль был успешно изменен"
        
        return error_handler, ldap.result['description']
    
    return "9", f"Нет доступа к изменению {model.identificator}"
    
def disable_emplooyee_status(model, new_status: 514): #-> тут деактивация статуса учетки
    base = f"ou={ldap_settings.USER_OU},{ldap_settings.BASE_DC}"
    print(base)
    search_filter = f"(pager={model.identificator})"
    print(search_filter)
    ldap.search(search_base=base, search_filter=search_filter, search_scope=SUBTREE, attributes=["pager"])

    if ldap.entries:
        current_dn = ldap.entries[0].entry_dn 
        res = check_member_of(current_dn, model)
        if res:
            print(f"Найден пользователь -- {current_dn}") #-> вывод для проверки результата
            ldap.modify(current_dn, {'userAccountControl': [(MODIFY_REPLACE, new_status)]})
            print(ldap.result)
        
            if ldap.result['description'] != "success":
                return error_handler(ldap.result['result']), 
            else:
                return "0", None
            
        return "9", f"Нет доступа к включению записи {model.identificator}"
        
    return "15", f"Нет пользователя: {model.identificator}"     
    
        
def change_params(model, params): #-> функция смены параметров сотрудника
    result, entries = search_all_user_params(model.identificator, ldap_settings.USER_OU, param="pager")  #-> проверка
    if entries is None or entries[0].entry_dn is None:
        return "15", "нет такого пользователя"
    
    if not check_member_of(entries[0].entry_dn, model):
        return "9", f"Нет доступа к изменению параметров у {model.identificator}"
    
    if not result:
        return "8", "Нет такого пользователя"
    
    
    change_values = create_dict_to_change_values(model, params) #-> при наличии необязательных параметров - добавляет элементы
    current_dn = entries[0].entry_dn
    print(ldap.entries)
    for key, val in change_values.items():
        ldap.modify(current_dn, {key: [(MODIFY_REPLACE, [val])]})
        if ldap.result['description']!="success":
                return error_handler(ldap.result['result']), ldap.result['description'] #-> ну а тут, возврат ошибки 
    return "0", None
        

def add_id(model): #-> добавление ид 1с в пользователя, который уже существует
    result, entries = search_all_user_params(model.userPrincipalName, ldap_settings.USER_OU, 'userPrincipalName')
    
    if result:
        user_dn = entries[0].entry_dn
        ldap.modify(user_dn, {'pager': [(MODIFY_REPLACE, [model.identificator])]})
        if ldap.result['description'] != "success":
            return "ошибка", str(ldap.result['description'])
        return "0", None
    return "15", f"Пользователя с таким ид и логином {model} нет"

def check_exist_ou(): #-> проверка существования ou
    search_filter = '(objectClass=organizationalUnit)'
    try:
        ldap.search(ldap_settings.BASE_DC, search_filter, search_scope=SUBTREE, attributes=['ou'])

        if ldap.entries:
            print("Доступные OU:")
            for entry in ldap.entries:
                print(entry.ou)
        else:
            print("OU не найдены.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def update_sAMAccountName(model):
    result, _ = search_all_user_params(model.new_sAMAccountName, ldap_settings.USER_OU, "sAMAccountName") #-> проверка, что такой логин не существует
    
    if result:
        return "4", f"Такой логин {model.new_sAMAccountName} уже существует, проверяют {model.identificator}"
    
    current_result, entries_current = search_all_user_params(model.identificator, ldap_settings.USER_OU, "pager") #-> проверка, что такой пользователь существует
    if not current_result:
        return "8", f"Пользователь с таким {model.identificator} не существует"
    
    employee_dn = entries_current[0].entry_dn
    if not check_member_of(employee_dn, model):
        return "9", f"Нет доступа к изменению логина у {model.identificator}"
    
    employee_dn = entries_current[0].entry_dn #-> адрес записи с пользователем
    ldap.modify(employee_dn, {'sAMAccountName': [MODIFY_REPLACE, [model.new_sAMAccountName]]})
     
    if ldap.result['description'] == "success":
        return "0", "Смена логина прошла успешно"
    
    return error_handler(ldap.result), f"При смене логина произошла ошибка: {ldap.result['description']}"

def search_all_user_params(user, ou_name, param): #-> получение/проверка наличия текущей записи, поиск по атрибуту
    ou_dn_adress = f"{ldap_settings.BASE_DC}"
    search_info = f"({param}={user})"
    print(search_info, ou_dn_adress)
    ldap.search(ou_dn_adress, search_info, attributes=['*']) #-> поиск всех атрибутов
    if ldap.entries:
        print("данные есть")
        print(ldap.entries)
        return True, ldap.entries

    return False, None

def search_user_info(user, ou_name, param): #-> получение/проверка наличия текущей записи, поиск по атрибуту
    ou_dn_adress = f"{ldap_settings.BASE_DC}"
    search_info = f"({param}={user})"
    print(search_info, ou_dn_adress)
    ldap.search(ou_dn_adress, search_info, search_scope=SUBTREE, attributes=['cn', 'sn', 'givenName','middleName', 'department', 'description', 'mobile', 'userAccountControl', 'mail', 'title', 'sAMAccountName']) #-> поиск всех атрибутов
    if ldap.entries:
        print("данные есть")
        print(ldap.entries)
        return True, ldap.entries
    return False, None


def check_member_of(user, model):
    print(user, model)
    
    ldap.search(f'{ldap_settings.BASE_DC}', f"(pager={model.identificator})", attributes=["memberOf"], search_scope=SUBTREE)
    print(ldap.entries, '')
    non_groups = file_reader()
    print(non_groups, "чего")
    
    if ldap.entries:
        if "memberOf" in ldap.entries[0].entry_attributes:
            all_groups = ldap.entries[0]["memberOf"].value
        else:
            all_groups = []
        
        print(type(all_groups), all_groups, '/AAAA')
        print(non_groups, '-')

        
        if type(all_groups) == str:
            print(all_groups in non_groups)
            if all_groups in non_groups:
                print("есть такое")
                return False
        
        if all_groups == [] or all_groups is None:
            return True
            
        if any(group in non_groups for group in all_groups): #-> в случае, если у пользователя больше 1 группы
            print("ничего нет")
            return False
        
        return True
    return True
#-----> все, что связано с группами пользователей
def check_group_exist(model): #-> проверка существования текущей группы
    group_filter = f'(cn={model.group_name})'
    ldap.search(ldap_settings.BASE_DC, group_filter, search_scope=SUBTREE, attributes=['*'])

    if ldap.entries:
        return True, ldap.entries
    
    return False, None

def print_group_members(model):
    result, entries = check_group_exist(model)
    if not result:
        return '000022393', 'Нет такой группы:)'
    
    group_dn = entries[0]
    members = group_dn.member.values if 'member' in group_dn else []
    
    all_members = list(members)
    
    print(f"Все участники группы {group_dn}:")
    for member in all_members:
        print(member)
    return '0', all_members

def change_employee_in_current_group(model, action): #-> добавление/удаление пользователя в группу
    result, entries = check_group_exist(model) #-> проверка существования группы
    if not result:
        return "16", ldap.result['description']
    
    employee_result, employee_entries = search_all_user_params(model.identificator, ldap_settings.USER_OU, "pager") #-> проверка существования пользователя
    print(employee_result)
    if not employee_result:
        return "15", ldap.result['description']

    employee_dn = employee_entries[0].entry_dn #-> адрес записи пользователя
    group_adress = entries[0].entry_dn #-> адрес записи группы
    
    if not check_member_of(employee_dn, model):
        return "9", f"Нет доступа к {action}"
    
    match(action):
        case "add_user": #-> добавление пользователя
            ldap.modify(group_adress, {'member': [(MODIFY_ADD, [employee_dn])]})
            if ldap.result['description'] == "success":
                return "0", None
            
            print(ldap.result)
            return error_handler(ldap.result['result']), f"При добавлении возникла ошибка: {ldap.result['description']}" 
               
        case "remove_user": #-> удаление пользователя
            ldap.modify(group_adress, {'member': [(MODIFY_DELETE, [employee_dn])]})
            if ldap.result['description'] == "success":
                return "0", None
            
            print(ldap.result)
            return error_handler(ldap.result['result']), f"При удалении пользователя возникла ошибка: {ldap.result['description']}"
        
    
# ------> функции, связанные с созданием organizational unit и подключению к ad
def create_new_ou(new_ou_name): #-> создание нового ou; результат - json
    print(ldap_settings.BASE_DC, new_ou_name)
    ou_dn_adress = f"OU={new_ou_name},{ldap_settings.BASE_DC}" #-> тут полный адрес для создания OrganizationalUnit
    print(ou_dn_adress)
    ou_attributes = {
    "objectClass": ["top", "organizationalUnit"], #-> необходимые базовые атрибуты (нет смысла добавлять доп. ObjClass)
    "ou": ou_dn_adress
    }
    
    if ldap.add(ou_dn_adress, attributes=ou_attributes): # проверка успешности добавления
        print(f'OU {ou_dn_adress} успешно создан.')
        return {"success" : True}
        
    return {"success" : False, 'message': ldap.last_error}


def create_dict_to_change_values(model, dict):
    change_values = {
        'title': model.employee_position,
        'department': model.department
    }
    
    for elem in dict.items():
        match(elem):
            case "phone_number":
                change_values["mobile"] = model.phone_number
            case "description":
                change_values["description"] = model.description
    
    return change_values
    
def create_add_dict(model):
    expected_attributes = {
                'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
                'cn': model.fullname,
                'givenName': model.name,
                'sn': model.surname,
                'displayName': model.fullname,  
                'mail': model.mail,
                'UserAccountControl': 514,
                'UserPrincipalName': str(model.userPrincipalName), 
                'sAMAccountName': model.sAMAccountName, 
                'Pager': model.identificator
            }
    if model.patronymic is None:
        return expected_attributes
    
    expected_attributes['middleName'] = model.patronymic
    return expected_attributes
        

def error_handler(exception):
    print(exception)
    exceptions_codes = {
        19: 10, #-> constraint violation, нарущена политика паролей (слабый пароль и тд)
        50: 12,
        16: 15, #-> нет пользователя в группе   
        32: 7, #-> no such object, объект не найден
        68: 8, #-> entry already exist
        34: 5, #-> invalid dn
        53: 13, #-> сервер откзазывается менять пароль
        52: 11 #-> сервер недоступен
        
    }
    print(exceptions_codes.get(exception))
    return exceptions_codes.get((exception))