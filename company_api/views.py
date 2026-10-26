from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Department,Employee,Project,Assignment,Asset
from .serializers import DepartmentSerializer,EmployeeSerializer,ProjectSerializer,AssignmentSerializer,AssetSerializer
class DepartmentViewSet(viewsets.ModelViewSet):
 queryset=Department.objects.all(); serializer_class=DepartmentSerializer
 search_fields=["name","location"]; ordering_fields=["name","created_at"]
class EmployeeViewSet(viewsets.ModelViewSet):
 queryset = Employee.objects.select_related("department").all().order_by("id"); serializer_class=EmployeeSerializer
 filterset_fields=["department","is_active"]; search_fields=["full_name","email","job_title","department__name"]; ordering_fields=["full_name","salary","created_at"]
class ProjectViewSet(viewsets.ModelViewSet):
 queryset=Project.objects.select_related("department").all(); serializer_class=ProjectSerializer
 filterset_fields=["department"]; search_fields=["name","description"]; ordering_fields=["name","start_date","created_at"]
class AssignmentViewSet(viewsets.ModelViewSet):
 queryset=Assignment.objects.select_related("employee","project").all(); serializer_class=AssignmentSerializer
 filterset_fields=["employee","project"]; search_fields=["role","employee__full_name","project__name"]; ordering_fields=["assigned_at","role"]
class AssetViewSet(viewsets.ModelViewSet):
 queryset=Asset.objects.select_related("assigned_to").all(); serializer_class=AssetSerializer
 filterset_fields=["status","asset_type","assigned_to"]; search_fields=["asset_tag","asset_type","manufacturer","model_number"]; ordering_fields=["asset_tag","asset_type","created_at"]
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request): return Response({"status":"ok","service":"Python REST API & Database Service"})
@api_view(["GET"])
def dashboard(request):
 return Response({"departments":Department.objects.count(),"employees":Employee.objects.count(),"projects":Project.objects.count(),"assignments":Assignment.objects.count(),"assets":Asset.objects.count(),"available_assets":Asset.objects.filter(status="available").count()})
