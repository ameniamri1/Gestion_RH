#gestion_conges\admin.py
from django.contrib import admin
from .models import Employee, Leave ,ApprovalLevel

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email', 'department')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'type_of_leave', 'start_date', 'end_date', 'status')
    #list_filter = ('type_of_leave', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'type_of_leave')
   # list_per_page = 100

@admin.register(ApprovalLevel)
class ApprovalLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')