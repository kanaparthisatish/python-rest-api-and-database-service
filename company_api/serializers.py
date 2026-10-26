from rest_framework import serializers
from .models import Department,Employee,Project,Assignment,Asset
class DepartmentSerializer(serializers.ModelSerializer):
 class Meta:
  model=Department
  fields="__all__"
  read_only_fields=["id","created_at"]
class EmployeeSerializer(serializers.ModelSerializer):
 department_name=serializers.CharField(source="department.name",read_only=True)
 class Meta:
  model=Employee
  fields=["id","full_name","email","department","department_name","job_title","salary","is_active","created_at"]
  read_only_fields=["id","created_at"]
 def validate_full_name(self,v):
  if not v.strip(): raise serializers.ValidationError("Name cannot be blank.")
  return v.strip()
 def validate_salary(self,v):
  if v<0: raise serializers.ValidationError("Salary cannot be negative.")
  return v
class ProjectSerializer(serializers.ModelSerializer):
 class Meta:
  model=Project
  fields="__all__"
  read_only_fields=["id","created_at"]
 def validate(self,a):
  start=a.get("start_date",getattr(self.instance,"start_date",None)); end=a.get("end_date",getattr(self.instance,"end_date",None))
  if start and end and end<start: raise serializers.ValidationError({"end_date":"End date cannot be before start date."})
  return a
class AssignmentSerializer(serializers.ModelSerializer):
 class Meta:
  model=Assignment
  fields="__all__"
  read_only_fields=["id","assigned_at"]
 def validate(self,a):
  employee=a.get("employee",getattr(self.instance,"employee",None)); project=a.get("project",getattr(self.instance,"project",None))
  if employee and project:
   qs=Assignment.objects.filter(employee=employee,project=project)
   if self.instance: qs=qs.exclude(pk=self.instance.pk)
   if qs.exists(): raise serializers.ValidationError("Employee is already assigned to this project.")
  return a
class AssetSerializer(serializers.ModelSerializer):
 class Meta:
  model=Asset
  fields="__all__"
  read_only_fields=["id","created_at"]
 def validate(self,a):
  status=a.get("status",getattr(self.instance,"status","available")); employee=a.get("assigned_to",getattr(self.instance,"assigned_to",None))
  if status=="assigned" and not employee: raise serializers.ValidationError({"assigned_to":"Assigned assets need an employee."})
  if status=="available" and employee: raise serializers.ValidationError({"assigned_to":"Available assets cannot have an employee."})
  return a
