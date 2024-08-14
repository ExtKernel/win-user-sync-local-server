from django.urls import path

from .views import (
    create_user,
    update_user_password,
    enable_user,
    disable_user,
    delete_user,
    get_users,
    get_user,
)

urlpatterns = [
    # Create
    path('create/', create_user, name='create_user'),

    # Read
    path('', get_users, name='get_users'),
    path('<str:username>/', get_user, name='get_user'),

    # Update
    path('update-password/<str:username>/', update_user_password, name='update_user_password'),
    path('enable/<str:username>/', enable_user, name='enable_user'),
    path('disable/<str:username>/', disable_user, name='disable_user'),

    # Delete
    path('delete/<str:username>/', delete_user, name='delete_user'),
]
