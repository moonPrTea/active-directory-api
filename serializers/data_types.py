from typing import Optional
from pydantic import BaseModel, Field

#-----> сотрудники и операции над ними
class AddEmployee(BaseModel): #-> добавление пользователя
    surname: str= Field(min_length=3, max_length=50)
    name: str= Field(min_length=3, max_length=50)
    patronymic: str = Field(default=None)
    sAMAccountName: str = Field() #-> smaaccount_name для ad, без cchgeu.ru
    userPrincipalName: str = Field(min_length=3)
    fullname: str = Field(min_length=3) #-> фио сотрудника
    password: str#-> пароль
    mail: str #-> почта сотрудника
    identificator: str = Field(min_length=3) 
    
class UpdateEmployeeStatus(BaseModel):
    identificator_1c: str
    
class ChangeEmployeeParams(BaseModel): #-> поменять атрибуты сотрудника
    #-> по установленным атрибутам - отдел, должность, внутренний телефон, описание (?)
    department: str = Field() #-> подразделение сотрудника
    employee_position: str = Field() #-> должность сотрудника
    identificator: str = Field(min_length=3)
    phone_number: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)

class ChangePassword(BaseModel): #-> смена пароля
    user_password: str = Field(min_length=8) #-> пароль
    identificator: str = Field(min_length=3)

class ChangesAMAccountName(BaseModel): #-> смена логина
    new_sAMAccountName: str
    identificator: str = Field(min_length=3)
    
#----> группы пользователей
class AppendGroupOfStuff(BaseModel):
    group_name: str #-> название группы
    description: str #-> описание группы
    valid_name: str #-> нормальное имя группы
    group_mail: str = Field(default=" ") #-> почта, в будущем для рассылок (?)

class AddOrDeleteGroupMember(BaseModel):
    group_name: str
    identificator: str

class AddId(BaseModel):
    userPrincipalName: str
    identificator: str

class PrintMembers(BaseModel):
    group_name: str

class AddOU(BaseModel):
    ou_name: str

    
    
    
    
   
            
    

    
    
    
    