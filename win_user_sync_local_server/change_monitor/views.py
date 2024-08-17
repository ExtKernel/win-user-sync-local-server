"""
This module contains view functions for managing the monitor.
"""

from django_keycloak_auth.decorators import keycloak_roles
from rest_framework.decorators import api_view
from django.http import JsonResponse

from config.settings.base import PRINCIPAL_ROLE_NAME
from win_user_sync_local_server.change_monitor.monitor import Monitor


monitor = Monitor()

@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def start_monitor(request):
    """Start the interval monitor."""
    try:
        interval = int(request.POST.get('interval', 3600))  # default to 1 hr if not specified
        monitor.start_interval_monitor(interval_in_sec=interval)
        return JsonResponse({
            'status': 'success',
            'message': f'Interval monitoring started with an interval of {interval} seconds'
        }, status=200)
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid interval value'
        }, status=400)
    except Exception as exc:
        return JsonResponse({
            'status': 'error',
            'message': f'Error starting monitor: {str(exc)}'
        }, status=500)


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def stop_monitor(request):
    """Stop the interval monitor."""
    try:
        monitor.stop_interval_monitor()
        return JsonResponse({
            'status': 'success',
            'message': 'Interval monitoring stopped'
        }, status=200)
    except Exception as exc:
        return JsonResponse({
            'status': 'error',
            'message': f'Error stopping monitor: {str(exc)}'
        }, status=500)
