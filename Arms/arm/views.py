from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,filters
from .models import Employee,Deployed,Pricipal_consultant,Employee_exit,OnbordsTable,Exit_raise,Company_propertise
from .forms import EmployeeForm
from .serializers import emp_serilizer,deply_serilizer,princple_serializer,UserSerializer, TokenPairSerializer,UserRegistrationSerializer,UserLoginSerializer,OnbordsTable_serializer,Company_propertise_serializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from datetime import date
from django.db.models import Max,F
from rest_framework.decorators import action
from django_filters import rest_framework as filters



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    serializer_class = TokenPairSerializer

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)




def register_employee(request):
    if request.method == 'POST':
        eform = EmployeeForm(request.POST)
        if eform.is_valid():
            eform.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/')
        else :
            messages.success(request, 'Form  not submitted ')
            return render(request,'register_employee.html',{'form':eform})
    else:
        eform =EmployeeForm()
        return render(request,'register_employee.html',{'form':eform})



class TechnologyCountAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        python_count = Employee.objects.filter(technology_cat='python').count()
        java_count = Employee.objects.filter(technology_cat='java').count()
        # reactjs_count = Employee.objects.filter(technology_cat='Reactjs').count()
        salesforce_count = Employee.objects.filter(technology_cat='Salesforce').count()
        counts = {
            'Python': python_count,
            'Java': java_count,
            'Salesforce': salesforce_count
        }
        return Response(counts)
    def post(self,request):
        return Response('this is post method')
    
class Counts_all_status(APIView):

    def get(self,request):
        result=[]
        technology_cat_list = Employee.objects.values_list('technology_cat', flat=True).distinct()
        employee_status_list = Employee.objects.values_list('employee_status', flat=True).distinct()
        for i in list(technology_cat_list):
            Counts_all_status={}
            for j in list(employee_status_list):
                Counts_all_status[j]=Employee.objects.filter(technology_cat=i,employee_status=j).count()
            result.append(Counts_all_status)
        return Response(result)        
    


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            token_pair = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            print(token_pair['access'])
            print(str(refresh.access_token))
            response = Response(token_pair, status=status.HTTP_200_OK)
            response.set_cookie('jwt_token', token_pair['access'], httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    

            
class Deployeddetails(APIView):
    def get(self, request,id):
        deploy_ins=Deployed.objects.get(id=id)
        emp_name = deploy_ins.employee.first_name
        return Response({"name" : emp_name})
    def post(self,request):
        return Response('this is post method')
    

class Employee_data(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = emp_serilizer
    queryset =Employee.objects.all()

class Deploy_data(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = deply_serilizer
    queryset =Deployed.objects.all()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['employee'].employee_status = 'Deployed'
        serializer.validated_data['employee'].save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UpdateEmployeeStatus(APIView):
    def get(self, request):
        # try:
        #     latest_project_end_dates = Deployed.objects.values('employee_id').annotate(latest_project_end_date=Max('project_end_date'))
        #     recently_completed_projects = latest_project_end_dates.filter(latest_project_end_date__lt=date.today(),employee__employee_status='Deployed')
        #     distinct_employee_ids = [record['employee_id'] for record in recently_completed_projects]
        #     updated_count = Employee.objects.filter(id__in=distinct_employee_ids).update(employee_status='On Bench')
        #     return Response({'message': f'{str(updated_count)} employee(s) status updated to On Bench'}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     print('this is exception function')
        #     return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            distinct_employee_ids = Deployed.objects.values('employee_id').annotate(
                latest_project_end_date=Max('project_end_date')
            ).filter(latest_project_end_date__lt=date.today(),employee__employee_status='Deployed').values_list('employee_id', flat=True)
            updated_count = Employee.objects.filter(id__in=distinct_employee_ids).update(employee_status='On Bench')
            return Response({'message': f'{updated_count} employee(s) status updated to On Bench'}, status=status.HTTP_200_OK)

        except Exception as e:
            print('An exception occurred:', e)
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class active_deployed_employees(viewsets.ModelViewSet):
    queryset=Deployed.objects.all()
    serializer_class=deply_serilizer
    def retrieve(self, request, *args, **kwargs):
        queryset=Deployed.objects.filter(employee__employee_status='Deployed')
        return super().retrieve(request, *args, **kwargs)
class Principle_data(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = princple_serializer
    queryset =Pricipal_consultant.objects.all()


class DeployedFilter(filters.FilterSet):
    class Meta:
        model = Deployed
        fields = {
            'employee__employee_status': ['exact'],
        }

class Deployed_Filters_Emp(viewsets.ModelViewSet):
    queryset = Deployed.objects.all()
    serializer_class = deply_serilizer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DeployedFilter
    ordering_fields = ['date_of_deploy']

    def get_queryset(self):
        return super().get_queryset().filter(employee__employee_status__in=['On Bench', 'Deployed'])

class OnbordsTable_view(viewsets.ModelViewSet):
    queryset=OnbordsTable.objects.all()
    serializer_class=OnbordsTable_serializer

class Onboard_to_Aja(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=emp_serilizer
    def create(self, request):
        data = request.data
        applicant_id = data.get('applicant_num')
        try:
            Onbords_details = OnbordsTable.objects.get(application_num=applicant_id)
            print(Onbords_details)
        except OnbordsTable.DoesNotExist:
            return Response({'error': 'Appliacant_details with provided ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
        employee_data = {
            'employee_id': data.get('employee_id'),
            'first_name': Onbords_details.first_name,
            'last_name': Onbords_details.last_name,
            'email': Onbords_details.email,
            'graduation': Onbords_details.graduation,
            'stream': Onbords_details.graduation_stream,
            'ug_year_of_passout': Onbords_details.graduation_year_of_passout,
            'pg_education': Onbords_details.pg_education,
            'pg_education_passout_year': Onbords_details.pg_education_passout_year,
            'pg_stram': Onbords_details.pg_stream,
            'mobile_no': Onbords_details.mobile_no,
            'alt_mobile_no': Onbords_details.alt_mobile_no,
            'designation': data.get('designation'),
            'date_of_join': data.get('date_of_join'),
            'technology_cat': data.get('technology_cat'),
            'employee_status': data.get('employee_status'),
            'remarks': data.get('remarks'),
            # 'blood_group':data.get('blood_group')
        }
        serializer = emp_serilizer(data=employee_data)
        if serializer.is_valid():
            serializer.save()
            Onbords_details.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Exit_Raise_view(APIView):
    def put(self,request,id):
        print(id)
        print(Exit_raise.objects.get(employee__employee_id=id))

        employee=Exit_raise.objects.get(employee__employee_id=id)
        employee.exit_raise = True  
        Employee_exit.exit_reason=request.data.get('exit_reason')
        employee.save() 
        return Response({"status":"succesfully Raised the request for Exit formalities"})

    def get(self,request):
        request_raised_employees=Exit_raise.objects.filter(exit_raise=True).values_list('employee__employee_id', flat=True)
        return Response(request_raised_employees) 
    
    def post(self,request,id):
        insta=Employee.objects.get(employee_id=id)
        Exit_raise.objects.create(employee=insta,exit_raise=False)
        return Response({"status":"You can raise the exit request"})
    
class Company_propertise_view(viewsets.ModelViewSet):
    serializer_class = Company_propertise_serializer
    queryset =Company_propertise.objects.all()

    





        


