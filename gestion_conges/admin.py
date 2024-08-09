#gestion_conges\admin.py
from django.contrib import admin
from .models import Employee, Leave ,ApprovalLevel,Attendance ,Department, Performance, Training



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

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'employee', 'work_hours', 'overtime_hours', 'date')
    search_fields = ('employee__user__username',)  # Champs sur lesquels rechercher
    list_filter = ('date',)  # Filtres disponibles dans la liste
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Correction des champs affichés


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'performance_score')  # Correction des champs affichés

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training_title', 'training_date')  # Correction des champs affichés
