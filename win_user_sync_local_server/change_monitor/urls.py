from django.urls import path

from . import views

urlpatterns = [
    path('start_monitor/', views.start_monitor, name='start_monitor'),
    path('stop_monitor/', views.stop_monitor, name='stop_monitor'),
]
