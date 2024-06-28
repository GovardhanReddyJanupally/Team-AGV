"""
URL configuration for Arms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from arm import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('emp_data',views.Employee_data,basename='emp_data')
router.register('Onboard_to_Aja',views.Onboard_to_Aja,basename='Onboard_to_Aja')
router.register('OnbordsTable',views.OnbordsTable_view,basename='OnbordsTable')
router.register('dpl_data',views.Deploy_data,basename='dpl_data')
router.register('ppl_data',views.Principle_data,basename='ppl_data')
router.register('cpv_data',views.Company_propertise_view,basename='cpv_data')
router.register('deployed_filters', views.Deployed_Filters_Emp, basename='Deployed_Filters_Emp')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('emp',views.register_employee,name='register_employee' ),
    path('technologycount',views.TechnologyCountAPIView.as_view(),name='tcp' ),
    path('dep/<int:id>',views.Deployeddetails.as_view(),name='dep' ),
    path('api/register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('api/token/', views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.UserDetailsView.as_view(), name='user_details'),
    path('api/login/', views.UserLoginView.as_view(), name='login'),
    path('e', views.UpdateEmployeeStatus.as_view(), name='update_employee_status'),
    path('exit_raise/<int:id>/', views.Exit_Raise_view.as_view(), name='exit_raise_put'),
    path('exit_raise/<int:id>/', views.Exit_Raise_view.as_view(), name='exit_raise_put'),
    path('exit_raise/', views.Exit_Raise_view.as_view(), name='exit_raise_get'),
    # path('',views.Employee_data.as_view),
    path('',include(router.urls)),

]
