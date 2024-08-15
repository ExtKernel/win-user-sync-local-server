from django_keycloak_auth.decorators import keycloak_roles
from rest_framework.decorators import api_view
from django.http import JsonResponse

from config.settings.base import PRINCIPAL_ROLE_NAME
from win_user_sync_local_server.change_monitor.monitor import Monitor


monitor = Monitor()

@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def start_monitor(request):
    interval = int(request.POST.get('interval', 3600))  # default to 1 hr if not specified
    monitor.start_interval_monitor(interval_in_sec=interval)
    return JsonResponse({'status': 'success', 'message': f'interval monitoring started with an interval of {interval} seconds'})


@keycloak_roles([PRINCIPAL_ROLE_NAME])
@api_view(['POST'])
def stop_monitor(request):
    monitor.stop_interval_monitor()
    return JsonResponse({"status": "success", "message": 'interval monitoring stopped'})
