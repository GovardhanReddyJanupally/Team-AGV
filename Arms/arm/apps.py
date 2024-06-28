from django.apps import AppConfig
from django.db.models.signals import pre_save
# from .signals import update_employee_status


class ArmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arm'

# class armConfig(AppConfig):
#     name = 'arm'
#     def ready(self):
#         pre_save.connect(update_employee_status, sender='arm.Deployed')
