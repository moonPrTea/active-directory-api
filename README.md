# active-directory-api

API implementation for integration with Active Directory

## Project Structure

1. **connection.py**  
Dependency for connecting to the Active Directory database.
A future update is planned to migrate to `Depends` with managed session injection

2. **ad_api.py**  
Contains all API routes currently used in the project

3. **structure_models.py**  
   Database relationship models. This file also initializes the DB session and creates tables if they do not already exist

4. **other_functions/**  
   Helper utilities extracted into a separate folder for better code organization

5. **data_types/**  
   Pydantic schemas (serializers) for request/response payloads.
Similar to routes, these schemas will be split into logical modules in future releases

6. **log.py**  
   Logging configuration and logic. Logging supports both file-based output and Telegram bot notifications

## Root Files

1. Configuration is stored in **.env**
2. API startup is handled in **main.py**
3. **requirements.txt** contains all project dependencies
4. **non_changed_groups** contains container/group names whose users have maximum privileges; account data for these users must remain unchanged