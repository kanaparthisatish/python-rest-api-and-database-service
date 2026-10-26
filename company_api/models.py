from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Department(models.Model):
 name=models.CharField(max_length=100,unique=True)
 location=models.CharField(max_length=120,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.name

class Employee(models.Model):
 full_name=models.CharField(max_length=120)
 email=models.EmailField(unique=True)
 department=models.ForeignKey(Department,on_delete=models.PROTECT,related_name="employees")
 job_title=models.CharField(max_length=100)
 salary=models.DecimalField(max_digits=12,decimal_places=2,validators=[MinValueValidator(0)])
 is_active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.full_name

class Project(models.Model):
 name=models.CharField(max_length=150)
 description=models.TextField(blank=True)
 department=models.ForeignKey(Department,on_delete=models.PROTECT,related_name="projects")
 start_date=models.DateField(null=True,blank=True)
 end_date=models.DateField(null=True,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=["name","department"],name="unique_project_per_department")]
 def clean(self):
  if self.start_date and self.end_date and self.end_date<self.start_date: raise ValidationError({"end_date":"End date cannot be before start date."})
 def __str__(self): return self.name

class Assignment(models.Model):
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="assignments")
 project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="assignments")
 role=models.CharField(max_length=100,default="Contributor")
 assigned_at=models.DateField(auto_now_add=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=["employee","project"],name="unique_employee_project_assignment")]

class Asset(models.Model):
 STATUS=[("available","Available"),("assigned","Assigned"),("maintenance","Maintenance")]
 asset_tag=models.CharField(max_length=50,unique=True)
 asset_type=models.CharField(max_length=80)
 manufacturer=models.CharField(max_length=100,blank=True)
 model_number=models.CharField(max_length=100,blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default="available")
 assigned_to=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name="assets")
 purchased_on=models.DateField(null=True,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 def clean(self):
  if self.status=="assigned" and not self.assigned_to: raise ValidationError({"assigned_to":"Assigned assets need an employee."})
  if self.status=="available" and self.assigned_to: raise ValidationError({"assigned_to":"Available assets cannot have an employee."})
