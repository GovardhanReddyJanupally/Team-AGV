from .models import Employee,Deployed,Employee_exit,Pricipal_consultant
from django.db import models
from django import forms
class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields = "__all__"

class DeployedForm(forms.ModelForm):
    class Meta:
        model=Deployed
        fields = "__all__"

class PricipalContentForm(forms.ModelForm):
    class Meta:
        model=Pricipal_consultant
        fields = "__all__"
class ExitForm(forms.ModelForm):
    class Meta :
        model = Employee_exit
        fields ="__all__"




