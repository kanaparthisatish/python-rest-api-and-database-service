from django.contrib import admin
from .models import Department,Employee,Project,Assignment,Asset
admin.site.register([Department,Employee,Project,Assignment,Asset])
