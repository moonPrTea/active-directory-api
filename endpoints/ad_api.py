from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from . import AddEmployee, AddOU, UpdateEmployeeStatus, ChangeEmployeeParams, ChangePassword, AppendGroupOfStuff, AddOrDeleteGroupMember, ChangesAMAccountName, Add1cId, PrintMembers
from . import create_new_ou, search_all_user_params, add_new_information, activate_employee_status, disable_emplooyee_status, change_params, update_password, change_employee_in_current_group, update_sAMAccountName, search_user_info, add_id, print_group_members
from . import check_headers #-> функция проверяет наличие нужного заголовка
from . import logger
from . import connecter

router = APIRouter(tags=['ad_api'])

@router.post("/add_new_employee", response_model=AddEmployee, response_class=JSONResponse) #-> для добавления пользователя
def insert_new_employee(model: AddEmployee, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        check_record, _ = search_all_user_params(model.userPrincipalName, "managed_users", param="cn") #-> проверка наличия логина
        print(check_record)
        if check_record:
            logger.error(f"IP: {request.client.host}\n\tКод: 4. Логин существует {model.userPrincipalName}")
            return JSONResponse({"returnCode": "4"}) #-> логин есть 
    
        check_id, _ = search_all_user_params(model.identificator, "managed_users", param="pager") #-> проверка наличия ид

        if check_id:
            logger.error(f"IP: {request.client.host}\n\tКод: 3. Id существует {model.identificator}")
            return JSONResponse({"returnCode": "3"}) #-> id физ лица есть  
          
        return_code, result, entries_result = add_new_information('managed_accounts', model)
        print(return_code, result, entries_result)
        if return_code is None or result is None:
            logger.error('')
        if return_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {return_code}. {result}\n Текст ошибки: {entries_result['description']}")
        
        return JSONResponse({"returnCode": return_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /add_new_employee\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})


@router.put('/activate_employee_record', response_model=UpdateEmployeeStatus, response_class=JSONResponse) #-> активация учетки
def update_status(model: UpdateEmployeeStatus, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        return_code, message = activate_employee_status(model, 512)
        
        if return_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {return_code}. Сообщение: {message}")
        
        return JSONResponse({"returnCode": return_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /activate_all_users\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.post('/get_info', response_model=UpdateEmployeeStatus, response_class=JSONResponse)
def get_info(model: UpdateEmployeeStatus, request: Request):
    result, code = check_headers(headers=request.headers)
    print(result, code)
    if result:
        result, entries = search_user_info(model.identificator, "managed_users", "pager")
        print(type(entries))
        if entries is None:
            return JSONResponse({"ответ": "НИЧЕГО НЕ НАЙДЕНО"})
        
        print(Request)
        return JSONResponse({"результат": str(entries)})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /activate_all_users\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.put('/add_id_to_ad_employee', response_model=Add1cId, response_class=JSONResponse) #--> добавление ид 1с
def add_1c_id(model: Add1cId, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        code, message = add_id(model)
        
        if code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {code}. Сообщение: {message}")
        
        return JSONResponse({"returnCode": code})
        
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /activate_all_users\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})
    
    
    
@router.put('/deactivate_employee_record', response_model=UpdateEmployeeStatus, response_class=JSONResponse) #-> деактивация учетки
def set_up_disable_value(model: UpdateEmployeeStatus, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        return_code, message = disable_emplooyee_status(model, 514)
        print(return_code, message)
        
        if return_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {return_code}. Сообщение: {message}")
        
        return JSONResponse({"returnCode": return_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /deactivate_employee_record\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.put('/change_employee_attributes', response_model=ChangeEmployeeParams, response_class=JSONResponse) #-> изменение параметров сотрудника
def activate_and_add_information(model: ChangeEmployeeParams, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        params = model.dict(exclude_none=True) #-> получение заполенных параметров
        print(params)
        error_code, message = change_params(model, params)
        if error_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод {error_code}. Текст {message}")
            
        return JSONResponse({"returnCode": error_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /change_employee_attributes\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.put('/update_password', response_model=ChangePassword, response_class=JSONResponse) #-> обновить пароль у пользователя
def update_user_password(model: ChangePassword, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        error_code, message = update_password(model)
        if error_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {error_code}. Текст: {message}")
            
        return JSONResponse({"returnCode": error_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /update_password\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.put('/update_login', response_model=ChangesAMAccountName, response_class=JSONResponse) #-> обновить логин у пользователя
def reset_sAMAccountName(model: ChangesAMAccountName, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        error_code, message = update_sAMAccountName(model)
        
        if error_code != 0:
            logger.error(f"IP: {request.client.host}\n\tКод: {error_code}. Сообщение {message}")
        
        return JSONResponse({"returnCode": error_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /update_login\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})  

#---> группы пользователей
@router.post('/add_new_employee_group', response_model=AppendGroupOfStuff, response_class=JSONResponse) #-> добавить группу пользователей
def insert_group(model: AppendGroupOfStuff, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        error_code, message = add_new_information("managed_groups", model)
        
        if error_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {error_code}. Сообщение {message}")
            
        return JSONResponse({"returnCode": error_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /add_new_employee_group\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})  

@router.put('/move_employee_to_group', response_model=AddOrDeleteGroupMember, response_class=JSONResponse) #-> добавить пользователя в группу
def append_employee(model: AddOrDeleteGroupMember, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        error_code, message = change_employee_in_current_group(model, "add_user")
            
        if error_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {error_code}. Сообщение {message}")
        return JSONResponse({"returnCode": error_code})     
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /move_employee_to_group\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.put('/drop_employee_from_group', response_model=AddOrDeleteGroupMember, response_class=JSONResponse) #-> удалить пользователя из группы
def delete_employee(model: AddOrDeleteGroupMember, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        error_code, message = change_employee_in_current_group(model, "remove_user")
        
        if error_code != "0":
            logger.error(f"IP: {request.client.host}\n\tКод: {error_code}. Сообщение {message}")
        return JSONResponse({"returnCode": error_code})
    
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /drop_employee_from_group\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code})

@router.post('/get_group_members', response_model=PrintMembers, response_class=JSONResponse) #-> вывести список участников групп в ад
async def print_members(model: PrintMembers, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        code, text = print_group_members(model)
        return JSONResponse({"returnCode": code, "members": text})
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /drop_employee_from_group\n Заголовки есть: {result}")
    return JSONResponse({"returnCode": code}) 

@router.post('/add_ou', response_model=AddOU, response_class=JSONResponse)
async def add_ou(model: AddOU, request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        elem = create_new_ou(model.ou_name)
        return JSONResponse(elem)
    return JSONResponse({"returnCode": code}) 
    
@router.get('/status')
async def get(request: Request):
    result, code = check_headers(headers=request.headers)
    if result:
        if connecter.is_active_connection():
            return JSONResponse({'returnCode': 0})
        
        success, error = connecter._reconnect()
        if success:
            return JSONResponse({'returnCode': 18})
        
        logger.error(f"IP: {request.client.host}\n\tСтатус {success}, маршрут: /status\n ошибка: {error}")
        return JSONResponse({'returnCode': 100})
    logger.error(f"IP: {request.client.host}\n\tКод {code}, маршрут: /status\n Заголовки есть: {result}")


#-> uvicorn название:website --reload 
#uvicorn application.views.user_api:website --host 0.0.0.0 --port 80 --reload