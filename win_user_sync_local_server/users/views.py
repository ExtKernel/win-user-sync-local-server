"""
This module contains views for user management operations.
"""

import json
from django.http import JsonResponse
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
        JsonResponse: A response with a success message or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400,
            content_type='application/json'
        )

    username = request_body.get('username')
    password = request_body.get('password')

    if not username:
        return JsonResponse(
            {"error": "Missing username parameter"},
            status=400,
            content_type='application/json'
        )

    try:
        if not password:
            user_editor.add(username, None)
        else:
            user_editor.add(username, password)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error creating user: {str(exc)}"},
            status=400,
            content_type='application/json'
        )

    return JsonResponse(
        {'message': f'User {username} was added successfully'},
        status=201,
        content_type='application/json'
    )


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_users(request):
    """
    API endpoint to retrieve all users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: A JSON response containing a list of all users.
    """
    try:
        users = user_retriever.get_all()
        serialized_users = [user.serialize() for user in users]
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error retrieving users: {str(exc)}"},
            status=500,
            content_type='application/json'
        )

    return JsonResponse(serialized_users, safe=False, content_type='application/json')


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['GET'])
def get_user(request, username):
    """
    API endpoint to retrieve a specific user by username.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the user to retrieve.

    Returns:
        JsonResponse: A JSON response containing the user's details.
    """
    try:
        user = user_retriever.get(username)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error retrieving user: {str(exc)}"},
            status=404,
            content_type='application/json'
        )

    return JsonResponse(user.serialize(), content_type='application/json')


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
        JsonResponse: A response with a success message or an error message.
    """
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400,
            content_type='application/json'
        )

    password = request_body.get('password')
    if not password:
        return JsonResponse(
            {"error": "Missing password parameter"},
            status=400,
            content_type='application/json'
        )

    try:
        user_editor.edit_password(username, password)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error updating password: {str(exc)}"},
            status=400,
            content_type='application/json'
        )

    return JsonResponse(
        {'message': f"User {username}'s password was updated successfully"},
        content_type='application/json'
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
        JsonResponse: A response with a success message.
    """
    try:
        user_editor.enable(username)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error enabling user: {str(exc)}"},
            status=400,
            content_type='application/json'
        )

    return JsonResponse(
        {'message': f'User {username} was enabled successfully'},
        content_type='application/json'
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
        JsonResponse: A response with a success message.
    """
    try:
        user_editor.disable(username)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error disabling user: {str(exc)}"},
            status=400,
            content_type='application/json'
        )

    return JsonResponse(
        {'message': f'User {username} was disabled successfully'},
        content_type='application/json'
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
        JsonResponse: A response with a success message.
    """
    try:
        user_editor.delete(username)
    except Exception as exc:
        return JsonResponse(
            {"error": f"Error deleting user: {str(exc)}"},
            status=400,
            content_type='application/json'
        )

    return JsonResponse(
        {'message': f'User {username} was deleted successfully'},
        content_type='application/json'
    )
