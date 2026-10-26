from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet,EmployeeViewSet,ProjectViewSet,AssignmentViewSet,AssetViewSet,health,dashboard
router=DefaultRouter()
router.register("departments",DepartmentViewSet,basename="department")
router.register("employees",EmployeeViewSet,basename="employee")
router.register("projects",ProjectViewSet,basename="project")
router.register("assignments",AssignmentViewSet,basename="assignment")
router.register("assets",AssetViewSet,basename="asset")
urlpatterns=[path("health/",health),path("dashboard/",dashboard),path("",include(router.urls))]
