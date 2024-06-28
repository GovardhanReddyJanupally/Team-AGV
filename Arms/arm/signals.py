
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Deployed, Employee

@receiver(pre_save, sender=Deployed)
def update_employee_status(sender, instance, **kwargs):
    print('this is signaled')
    if instance.project_end_date < timezone.now().date():
        employee = instance.employee
        employee.employee_status = 'On Bench'
        employee.save(update_fields=['employee_status'])
    else :
        employee = instance.employee
        employee.employee_status = 'Deployed'
        employee.save(update_fields=['employee_status'])
