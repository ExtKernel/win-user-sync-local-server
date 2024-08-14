from django_keycloak_auth.decorators import keycloak_roles
from rest_framework.decorators import api_view
from django.http import JsonResponse

from config.settings.base import PRINCIPAL_ROLE_NAME
from .monitor import start_interval_monitor, stop_interval_monitor


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def start_monitor(request):
    interval = int(request.GET.get('interval', 3600))
    start_interval_monitor(interval)
    return JsonResponse({'status': 'success', 'message': f'interval monitoring started with an interval of {interval} seconds'})


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def stop_monitor(request):
    stop_interval_monitor()
    return JsonResponse({"status": "success", "message": 'interval monitoring stopped'})
