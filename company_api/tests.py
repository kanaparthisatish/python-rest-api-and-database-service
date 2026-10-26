from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Department,Employee,Project,Assignment,Asset
class APITests(TestCase):
 def setUp(self):
  self.client=APIClient()
  user=get_user_model().objects.create_user(username="tester",password="test-pass-123")
  self.client.force_authenticate(user=user)
  self.dept=Department.objects.create(name="Engineering")
  self.emp=Employee.objects.create(full_name="Ananya Rao",email="ananya@example.com",department=self.dept,job_title="Developer",salary=Decimal("45000"))
  self.project=Project.objects.create(name="Portal",department=self.dept)
 def test_health(self):
  r=APIClient().get("/api/health/"); self.assertEqual(r.status_code,200); self.assertEqual(r.data["status"],"ok")
 def test_employee_list(self):
  r=self.client.get("/api/employees/"); self.assertEqual(r.status_code,200); self.assertEqual(r.data["count"],1)
 def test_create_employee(self):
  r=self.client.post("/api/employees/",{"full_name":"Ravi Kumar","email":"ravi@example.com","department":self.dept.id,"job_title":"QA","salary":"30000"},format="json"); self.assertEqual(r.status_code,201)
 def test_duplicate_email(self):
  r=self.client.post("/api/employees/",{"full_name":"Other","email":"ananya@example.com","department":self.dept.id,"job_title":"QA","salary":"30000"},format="json"); self.assertEqual(r.status_code,400)
 def test_search(self):
  r=self.client.get("/api/employees/?search=Ananya"); self.assertEqual(r.status_code,200); self.assertEqual(r.data["count"],1)
 def test_dashboard(self):
  r=self.client.get("/api/dashboard/"); self.assertEqual(r.status_code,200); self.assertEqual(r.data["employees"],1)
 def test_asset_validation(self):
  r=self.client.post("/api/assets/",{"asset_tag":"LAP-1","asset_type":"Laptop","status":"assigned"},format="json"); self.assertEqual(r.status_code,400)
