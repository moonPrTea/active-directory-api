# active-directory-api

REST API for managing Active Directory users and groups


## Configuration
Before running the application, configure required properties in 
```.env```

## Quick Start
### 1. Start infrastructure (Active directory in Samba)
```bash
docker compose up -d
```

### 2. Start python project
```bash
pip install -r requirements.txt
python3 main.py
```

## API Routes

### **Router prefix:** `/employee`

| Method  | URL                                          | Description                                                                                                                    |
|---------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `POST`  | `/employee`                                  | Create an employee. On success returns `201` with `status: CREATED_WITH_PASSWORD`. On failure returns `400`                    |
| `PATCH` | `/employee`                                  | Update employee data. On success returns `status: OPERATION_PERFORMED`. Returns `404` if user not found, `502` on other errors |
| `PATCH` | `/employee/activate/{user_principal_name}`   | Activate an employee account by `user_principal_name`. Returns `404` if user not found                                         |
| `PATCH` | `/employee/deactivate/{user_principal_name}` | Deactivate an employee account by `user_principal_name`. Returns `404` if user not found                                       |
| `PATCH` | `/employee/user_principal_name`              | Update `user_principal_name`. Returns `404` if user not found                                                                  |


### Example `/employee` requests

1. Create an employee
```bash
curl -s -X POST "http://0.0.0.0:80/employee" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Tom",
    "second_name": "Hardy",
    "middle_name": "Edward",
    "sAMAccountName": "thardy",
    "userPrincipalName": "tom.hardy@example.local",
    "password": "tomPassw$@b1",
    "email": "tom.hardy@example.local"
  }'
```

2. Update employee data
```bash
curl -s -X PATCH "http://0.0.0.0:80/employee" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "userPrincipalName": "tom.hardy@example.local",
    "department": "film department",
    "position": "Actor",
    "phone_number": "+491932913991"
  }'
```

3. Activate employee record
```bash
curl -s -X PATCH "http://0.0.0.0:80/employee/activate/tom.hardy%40example.local" \
  -H "Authorization: <LDAP_AUTH_TOKEN>"
```

4. Deactivate employee record
```bash
curl -s -X PATCH "http://0.0.0.0:80/employee/deactivate/tom.hardy%40example.local" \
  -H "Authorization: <LDAP_AUTH_TOKEN>"
```

5. Change userPrincipalName
```bash
curl -s -X PATCH "http://0.0.0.0:80/employee/user_principal_name" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_principal_name": "tom.hardy@example.local",
    "new_user_principal_name": "tom.hardy.new@example.local"
  }'
```

### **Router prefix:** `/employee_group`

| Method   | URL                                    | Description                                                                                                                         |
|----------|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `GET`    | `/employee_group/members/{group_name}` | Get all group members by group name                                                                                                 |
| `POST`   | `/employee_group`                      | Create an employee group. Returns `status` with the operation result                                                                |
| `PUT`    | `/employee_group/add_member`           | Add an employee in group. On success returns `status: OPERATION_PERFORMED`. Returns `404` if the operation cannot be performed      |
| `DELETE` | `/employee_group/delete_member`        | Delete an employee from group. On success returns `status: OPERATION_PERFORMED`. Returns `404` if the operation cannot be performed |

### Example `/employee_group` requests
1. Create employee group
```bash
curl -s -X POST "http://0.0.0.0:80/employee_group" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "actors",
    "description": "Good film actors"
  }'
```

2. Add employee to group
```bash
curl -s -X PUT "http://0.0.0.0:80/employee_group/add_member" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "actors",
    "user_principal_name": "tom.hardy.new@example.local"
  }'
```

3. Get all group members
```bash
curl -s "http://0.0.0.0:80/employee_group/members/actors" \
  -H "Authorization: <LDAP_AUTH_TOKEN>"
```

4. Remove employee from group
```bash
curl -s -X DELETE "http://0.0.0.0:80/employee_group/delete_member" \
  -H "Authorization: <LDAP_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "actors",
    "user_principal_name": "tom.hardy.new@example.local"
  }'
```
