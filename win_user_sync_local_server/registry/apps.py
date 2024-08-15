from django.apps import AppConfig
from py_eureka_client import eureka_client

from config.settings.base import EUREKA_URL, SERVER_NAME, get_server_host

def initialize_eureka():
    ip, port = get_server_host()

    # The following code will register your server to eureka server and also start to send heartbeat every 30 seconds
    if eureka_client.init(eureka_server=str(EUREKA_URL),
                          app_name=SERVER_NAME,
                          instance_port=int(port)):
        quit()


class RegistryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registry'

    def ready(self):
        initialize_eureka()
