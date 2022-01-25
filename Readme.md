# Task Assignment Chat System
Its a task assignment with status monitoring and inner real time chat support.

### How to run this project:
### Prequisite
* You should have Python installed on your Machine.
Now Open Terminal or Shell.

### Steps:
1. ```python3 -m venv env```
2. If on mac or linux: ```source env/bin/activate```. Windows: ```.\env\scripts\activate```
3. ``` python -m pip install requirements.txt ```
4. ``` python manage.py runserver ```


## Endpoints:

### Authentication urls 
``` 
 Registr Schema [GET] - /api/register/schema/?format=json
 Register [POST] - /api/register/
 Login Schema [GET] - /api/login/schema/?format=json
 Login [POST] - /api/login/
```

### Task urls 
``` 
 Task Schema [GET] - /api/task/schema/?format=json
 Task [POST, GET] - /api/task/
 Task [GET, PUT, DELETE] - /api/task/<id>
```

## Making Request on Endpoints:
### Regsiter - [POST]
```
{
    "username":"<username>",
    "password":"<password>"
}
```
### Login - [POST]
```
{
    "username":"<username>",
    "password":"<password>"
}
```
### Task - [POST] 
(Note: Upon login you'll receive APIKey. Use it in the authorization header, then make this request.)
```Authorization: ApiKey <username>:<api_key>```
```
{
    "title":"<title>",
    "description":"<description>"
}
```

#### Full Schema:
```
{
    "title":"<title>",
    "description":"<description>",
    "status":"<status>",
    "progress":"<progress>",
    "assigned_to":[]
}
```