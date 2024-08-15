# Windows User Synchronization Server
A Python-based server for managing Windows users and groups. This app is supposed to be used in a pair with [Identity Provider Synchronization Service
](https://github.com/ExtKernel/idp-sync-service), but it's okay to use standalone.

## Endpoints
Every endpoint requires an OAuth2 Bearer token retrieved from the Keycloak OAuth2 provider.

## User
### Create
Endpoint: `POST /users/create/`

JSON request body explanation:
```json
{
  "username": "username",
  "password": "plain-text-password" (optional)
}
```

### Get all users
Endpoint: `GET /users/`

### Get user
Endpoint: `GET /users/<username>/`

### Update user password
Endpoint: `PATCH /users/update-password/<username>/`

JSON request body explanation:
```json
{
  "password": "plain-text-password"
}
```

### Enable user
Endpoint: `PATCH /users/enable/<username>/`

### Disable user
Endpoint: `PATCH /users/disable/<username>/`

### Delete user 
Endpoint: `PATCH /users/delete/<username>/`

## User group
### Create
Endpoint: `POST /groups/create/`

JSON request body explanation:
```json
{
  "name": "usergroup-name",
  "description": "description" (optional)
  "users": ["username0", "username1"] (optional)
}
```

### Get all user groups
Endpoint: `GET /groups/`

### Get user group
Endpoint: `GET /groups/<usergroup-name>/`

### Get user group members
Endpoint: `GET /groups/<usergroup-name>/users/`

### Get members included in the user group
Endpoint: `GET /groups/<usergroup-name>/included-users/`

This endpoint expects a request body like described below and returns users that are members of the user group. 

JSON request body explanation:
```json
{
  "users": ["username0", "username1", "username2"]
}
```

### Rename user group
Endpoint: `PATCH /groups/rename/<usergroup-name>/`

JSON request body explanation:
```json
{
  "name": "some-new-name"
}
```

### Add a member to the user group
Endpoint: `PATCH /groups/add-user/<usergroup-name>/<username>/`


### Delete user group
Endpoint: `DELETE /groups/delete/<usergroup-name>/`

### Remove a user group member
Endpoint: `DELETE /groups/remove-user/<usergroup-name>/<username>/`

## Monitor
A change monitor. Checks if groups and users match the database on the [remote](https://github.com/ExtKernel/idp-sync-service). 
If you're using this server without an intent to reach the [remote](https://github.com/ExtKernel/idp-sync-service), 
please, don't try to call following endpoints. Especially, if you've set corresponding environment variables to empty or dummy values.

### Start the monitor
Endpoint: `POST /monitor/start_monitor/`

URL parameters: `interval`

This will start the monitoring of users and groups once in `interval` or 1 hour if the `interval` is not specified. 
Basically, this server will request groups and the client blacklist from the [remote](https://github.com/ExtKernel/idp-sync-service),
filter local entries according to the blacklist and check if the local entries array has the same length.

**Warning**: to avoid errors, ID of the client (which represents this server) registered on the [remote](https://github.com/ExtKernel/idp-sync-service)
should match the value of the `SERVER_NAME` environment variable.

### Stop the monitor
Endpoint: `POST /monitor/stop_monitor/`

## Configuration
This section describes the environment variables used by the server.

### General
- `SERVER_NAME` - the name of this server. **BE AWARE**: 
  - It'll be used as a service name to register in Eureka
  - It'll be used to reach the corresponding client on the [remote](https://github.com/ExtKernel/idp-sync-service) to retrieve its blacklists. The variable should match the ID of the client registered in the [remote](https://github.com/ExtKernel/idp-sync-service)
- `DJANGO_SECRET_KEY` - you can refer to this [topic](https://stackoverflow.com/a/57678930/23531217) for instructions
- `EUREKA_URL` - the full URL of the Eureka server. This variable has a default value: `http://localhost:8761/eureka`. But very likely will be required to be changed depending on your specific setup

### OAuth2 (Keycloak)
- `PRINCIPAL_ROLE_NAME` - the role that the OAuth2 user should have to access `secured` endpoints. Has a default value: `administrator`. **Note that** the token used to access this app should contain the role
- `KC_HOST` - the host of the Keycloak server
- `KC_REALM` - the `Realm` that the associated with this application client on the Keycloak server belongs to
- `KC_CLIENT_ID` - the `client ID` associated with this application's client on the Keycloak server
- `KC_CLIENT_SECRET` - the client `client secret` associated with this application's client on the Keycloak server

### [Remote's](https://github.com/ExtKernel/idp-sync-service) OAuth2
For standalone usage set following variables to empty or dummy values
- `REMOTE_SERVICE_OAUTH2_TOKEN_URL` - the `token url` of the OAuth2 provider that the [remote](https://github.com/ExtKernel/idp-sync-service) is registered in
- `REMOTE_SERVICE_OAUTH2_CLIENT_ID` - the `client ID` of the client that represents the [remote](https://github.com/ExtKernel/idp-sync-service) in the OAuth2 provider that it's registered in
- `REMOTE_SERVICE_OAUTH2_CLIENT_SECRET` - the `client secret` of the client that represents the [remote](https://github.com/ExtKernel/idp-sync-service) in the OAuth2 provider that it's registered in
- `REMOTE_SERVICE_OAUTH2_USERNAME` - the `username` of the user that is authorized to access the client that represents the [remote](https://github.com/ExtKernel/idp-sync-service) in the OAuth2 provider that it's registered in
- `REMOTE_SERVICE_OAUTH2_PASSWORD` - the `password` of the user that is authorized to access the client that represents the [remote](https://github.com/ExtKernel/idp-sync-service) in the OAuth2 provider that it's registered in

## Usage
### Django runserver
1) Clone the repository:
    ```bash
      git clone https://github.com/ExtKernel/win-user-sync-local-server.git
    ```
2) Navigate to the directory:
    ```bash
      cd win-user-sync-local-server
    ```
3) Create a virtual environment:
    ```bash
      python -m venv venv
    ```
4) Activate the environment:
    ```bash
      source venv/bin/activate
    ```
5) Install dependencies:
    ```bash
      pip install -r requirements.txt
    ```
6) Run the server:
    ```bash
      python manage.py runserver <host:port> --settings=config.settings.<desired-settings-config>
    ```
   For `<desired-settings-config>` you can choose either from `local` or `production`

### Docker
1) Pull the image:
    ```bash
      docker pull exkernel/win-user-sync-server:<VERSION>
    ```
2) Run the container:
    ```bash
      docker run --name=win-user-sync-server -p 8000:8000 exkernel/win-user-sync-server:<VERSION>
    ```
   - You can map any external port you want to the internal one
   - You can give any name to the container
    Remember to specify environment variables using the `-e` flag:
   - `-e SERVER_NAME`
   - `-e EUREKA_URL`
   - `-e PRINCIPAL_ROLE_NAME`
   
   You may also specify the optional ones if you want:
   - `-e REMOTE_SERVICE_OAUTH2_TOKEN_URL`
   - `-e REMOTE_SERVICE_OAUTH2_CLIENT_ID`
   - `-e REMOTE_SERVICE_OAUTH2_CLIENT_SECRET`
   - `-e REMOTE_SERVICE_OAUTH2_USERNAME`
   - `-e REMOTE_SERVICE_OAUTH2_PASSWORD`
   