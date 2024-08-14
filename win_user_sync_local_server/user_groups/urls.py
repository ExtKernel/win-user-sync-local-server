from django.urls import path

from .views import (
    create_usergroup,
    get_usergroup,
    get_usergroups,
    get_usergroup_users,
    get_included_in_usergroup_users,
    rename_usergroup,
    add_user_to_usergroup,
    delete_usergroup,
    remove_user_from_usergroup
)

urlpatterns = [
    # Create
    path('create/', create_usergroup, name='create_usergroup'),

    # Read
    path('<str:usergroup_name>/', get_usergroup, name='get_usergroup'),
    path('', get_usergroups, name='get_usergroups'),
    path('<str:usergroup_name>/users/', get_usergroup_users, name='get_usergroup_users'),
    path('<str:usergroup_name>/included-users/', get_included_in_usergroup_users, name='get_included_in_usergroup_users'),

    # Update
    path('rename/<str:usergroup_name>/', rename_usergroup, name='rename_usergroup'),
    path('add-user/<str:usergroup_name>/<str:username>/', add_user_to_usergroup, name='add_user_to_group'),

    # Delete
    path('delete/<str:usergroup_name>/', delete_usergroup, name='delete_usergroup'),
    path('remove-user/<str:usergroup_name>/<str:username>/', remove_user_from_usergroup, name='remove_user_from_usergroup'),
]
