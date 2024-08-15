import json

from django.http import HttpResponse
from django_keycloak_auth.decorators import keycloak_roles
from rest_framework.decorators import api_view

from config.settings.base import get_powershell_path, PRINCIPAL_ROLE_NAME
from .usergroups_scripts import UsergroupEditor, UsergroupRetriever


# Initialize UsergroupEditor and UsergroupRetriever with the PowerShell path
usergroups_editor = UsergroupEditor(get_powershell_path())
usergroups_retriever = UsergroupRetriever(get_powershell_path())


def check_name_presence(request_body):
    """
    Checks if the 'name' key is present in the request body.

    Args:
        request_body (dict): The request body.

    Returns:
        bool: True if 'name' is present, False otherwise.
    """
    return bool(request_body.get('name'))


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def create_usergroup(request):
    """
    API endpoint to create a new user group.

    Expects a JSON body with 'name' and optionally 'description' and 'users'.

    Args:
        request (HttpRequest): The request object containing the JSON body.

    Returns:
        HttpResponse: A response with the details of the created user group or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({"error": "Invalid JSON body"}), status=400, content_type="application/json")

    usergroup_name = request_body.get('name')
    if usergroup_name is None:
        return HttpResponse(json.dumps({"error": "Missing name parameter"}), status=400,
                            content_type="application/json")

    description = request_body.get('description')
    users = request_body.get('users')

    usergroups_editor.add(usergroup_name, description=description, users=users)

    response_data = {
        'usergroup': usergroup_name
    }

    if description:
        response_data['description'] = description
    if users:
        response_data['users'] = users
    response_data['message'] = f"User group '{usergroup_name}' was added successfully"

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_usergroup(request, usergroup_name):
    """
    API endpoint to retrieve a specific user group by name.

    Args:
        request (HttpRequest): The request object.
        usergroup_name (str): The name of the user group to retrieve.

    Returns:
        HttpResponse: A JSON response containing the user group's details.
    """
    usergroup = usergroups_retriever.get(usergroup_name)
    usergroup_serialized = usergroup.serialize()
    return HttpResponse(json.dumps(usergroup_serialized), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_usergroups(request):
    """
    API endpoint to retrieve all user groups.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A JSON response containing a list of all user groups.
    """
    usergroups = [usergroup.serialize() for usergroup in usergroups_retriever.get_all()]
    return HttpResponse(json.dumps(usergroups), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_usergroup_users(request, usergroup_name):
    """
    API endpoint to retrieve all users in a specific user group.

    Args:
        request (HttpRequest): The request object.
        usergroup_name (str): The name of the user group whose users are to be retrieved.

    Returns:
        HttpResponse: A JSON response containing the list of users in the user group.
    """
    users = [user.serialize() for user in usergroups_retriever.get_users(usergroup_name)]
    return HttpResponse(json.dumps(users), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_included_users(request, usergroup_name):
    """
    API endpoint to retrieve users from the given list who are included in a specific user group.

    Expects a JSON body with 'users'.

    Args:
        request (HttpRequest): The request object containing the JSON body.
        usergroup_name (str): The name of the user group.

    Returns:
        HttpResponse: A JSON response containing the list of included users or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({"error": "Invalid JSON body"}), status=400, content_type="application/json")

    included_users = usergroups_retriever.get_included_users(usergroup_name, request_body['users'])
    included_users_serialized = [user.serialize() for user in included_users]
    return HttpResponse(json.dumps({
        'usergroup': usergroup_name,
        'included_users': included_users_serialized
    }), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['PATCH'])
def rename_usergroup(request, usergroup_name):
    """
    API endpoint to rename a specific user group.

    Expects a JSON body with 'name'.

    Args:
        request (HttpRequest): The request object containing the JSON body.
        usergroup_name (str): The current name of the user group to be renamed.

    Returns:
        HttpResponse: A response with a success message or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({"error": "Invalid JSON body"}), status=400, content_type="application/json")

    if check_name_presence(request_body):
        new_name = request_body['name']
        usergroups_editor.rename(usergroup_name, new_name)
        return HttpResponse(json.dumps({
            'message': f'User group {usergroup_name} was successfully renamed to {new_name}'
        }), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"error": "Missing name parameter"}), status=400,
                            content_type="application/json")


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['PATCH'])
def add_user_to_usergroup(request, usergroup_name, username):
    """
    API endpoint to add a user to a specific user group.

    Args:
        request (HttpRequest): The request object.
        usergroup_name (str): The name of the user group.
        username (str): The username of the user to be added.

    Returns:
        HttpResponse: A response with a success message.
    """
    usergroups_editor.add_users(usergroup_name, [username])
    return HttpResponse(json.dumps({
        'message': f'{username} user was added successfully to group {usergroup_name}'
    }), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['DELETE'])
def delete_usergroup(request, usergroup_name):
    """
    API endpoint to delete a specific user group.

    Args:
        request (HttpRequest): The request object.
        usergroup_name (str): The name of the user group to be deleted.

    Returns:
        HttpResponse: A response with a success message.
    """
    usergroups_editor.delete(usergroup_name)
    return HttpResponse(json.dumps({
        'message': f'User group {usergroup_name} was successfully deleted'
    }), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['DELETE'])
def remove_user_from_usergroup(request, usergroup_name, username):
    """
    API endpoint to remove a user from a specific user group.

    Args:
        request (HttpRequest): The request object.
        usergroup_name (str): The name of the user group.
        username (str): The username of the user to be removed.

    Returns:
        HttpResponse: A response with a success message.
    """
    usergroups_editor.remove_user(usergroup_name, username)
    return HttpResponse(json.dumps({
        'message': f'User was successfully deleted from group {usergroup_name}'
    }), content_type='application/json')

