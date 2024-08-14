import json

from django.http import HttpResponse
from django_keycloak_auth.decorators import keycloak_roles
from rest_framework.decorators import api_view

from config.settings.base import get_powershell_path, PRINCIPAL_ROLE_NAME
from .user_scripts import UserRetriever, UserEditor


# Initialize UserEditor and UserRetriever with the PowerShell path
user_editor = UserEditor(get_powershell_path())
user_retriever = UserRetriever(get_powershell_path())


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def create_user(request):
    """
    API endpoint to create a new user.

    Expects a JSON body with 'username' and optionally 'password'.

    Args:
        request (HttpRequest): The request object containing the JSON body.

    Returns:
        HttpResponse: A response with a success message or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({"error": "Invalid JSON body"}), content_type='application/json', status=400)

    username = request_body.get('username')
    password = request_body.get('password')

    if not username:
        return HttpResponse(json.dumps({"error": "Missing username parameter"}),
                            content_type='application/json', status=400)
    elif not password:
        user_editor.add(username, None)
    else:
        user_editor.add(username, password)

    return HttpResponse(
        json.dumps({
            'message': f'User {username} was added successfully'
        }), content_type='application/json'
    )


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_users(request):
    """
    API endpoint to retrieve all users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A JSON response containing a list of all users.
    """
    users = user_retriever.get_all()
    serialized_users = [user.serialize() for user in users]

    return HttpResponse(json.dumps(serialized_users), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_user(request, username):
    """
    API endpoint to retrieve a specific user by username.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the user to retrieve.

    Returns:
        HttpResponse: A JSON response containing the user's details.
    """
    user = user_retriever.get(username)

    return HttpResponse(json.dumps(user.serialize()), content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['PATCH'])
def update_user_password(request, username):
    """
    API endpoint to update the password of a specific user.

    Expects a JSON body with 'password'.

    Args:
        request (HttpRequest): The request object containing the JSON body.
        username (str): The username of the user whose password is to be updated.

    Returns:
        HttpResponse: A response with a success message or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({"error": "Invalid JSON body"}), content_type='application/json', status=400)

    password = request_body.get('password')
    if not password:
        return HttpResponse(json.dumps({"error": "Missing password parameter"}), content_type='application/json',
                            status=400)

    user_editor.edit_password(username, password)

    return HttpResponse(
        json.dumps({
            'message': f'User {username}\'s password was updated successfully'
        }), content_type='application/json'
    )


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['PATCH'])
def enable_user(request, username):
    """
    API endpoint to enable a specific user.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the user to enable.

    Returns:
        HttpResponse: A response with a success message.
    """
    user_editor.enable(username)

    return HttpResponse(
        json.dumps({
            'message': f'User {username} was enabled successfully'
        }), content_type='application/json'
    )


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['PATCH'])
def disable_user(request, username):
    """
    API endpoint to disable a specific user.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the user to disable.

    Returns:
        HttpResponse: A response with a success message.
    """
    user_editor.disable(username)

    return HttpResponse(
        json.dumps({
            'message': f'User {username} was disabled successfully'
        }), content_type='application/json'
    )


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['DELETE'])
def delete_user(request, username):
    """
    API endpoint to delete a specific user.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the user to delete.

    Returns:
        HttpResponse: A response with a success message.
    """
    user_editor.delete(username)

    return HttpResponse(
        json.dumps({
            'message': f'User {username} was deleted successfully'
        }), content_type='application/json'
    )
