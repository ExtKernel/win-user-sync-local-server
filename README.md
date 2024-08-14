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

### Update user password
Endpoint: `PATCH /groups/update-password/<username>/`

JSON request body explanation:
```json
{
  "password": "plain-text-password"
}
```

### Enable user
Endpoint: `PATCH /groups/enable/<username>/`

### Disable user
Endpoint: `PATCH /groups/disable/<username>/`

### Delete user 
Endpoint: `PATCH /groups/delete/<username>/`
