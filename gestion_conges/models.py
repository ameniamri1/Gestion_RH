#gestion_conges\models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


default_user_id = settings.DEFAULT_USER_ID
class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other')
    address = models.TextField(null=True, blank=True, default='')
    phone_number = models.CharField(max_length=20, null=True, blank=True, default='')
    email = models.EmailField(unique=True, default='example@example.com')
    photo_url = models.CharField(max_length=255, null=True, blank=True, default='')
    department = models.CharField(max_length=100, default='Unassigned')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Leave(models.Model):
    TYPE_CHOICES = [
        ('maladie', 'Congés maladie'),
        ('vacances', 'Congés vacances'),
        ('maternité', 'Congés maternité'),
        ('sabbatique', 'Congés sabbatique'),
    ]

    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejettee', 'Rejetée'),
    ]
    type_of_leave = models.CharField(max_length=50, choices=TYPE_CHOICES, default='maladie')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True, default='')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    comments = models.TextField(blank=True, null=True, default='')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')

    def __str__(self):
        return f"{self.employee} - {self.get_type_of_leave_display()} du {self.start_date} au {self.end_date}"

    def get_type_of_leave_display(self):
        # Implémentez cette méthode si nécessaire
        return self.status

class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'gestion_conges_department'
    

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    performance_score = models.IntegerField()
    review_date = models.DateField()

    def __str__(self):
        return f'{self.employee} - {self.performance_score} - {self.review_date}'

class Training(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_title = models.CharField(max_length=200)
    training_date = models.DateField()

    def __str__(self):
        return f'{self.employee} - {self.training_title}'
    
class ApprovalLevel(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(unique=True)  # Niveau d'approbation (1, 2, 3, ...)
    approvers = models.ManyToManyField(User, related_name='approval_levels')  # Utilisateurs qui peuvent approuver à ce niveau

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_hours = models.TimeField()
    overtime_hours = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"Attendance {self.attendance_id} for {self.employee.name} on {self.date}"

class Absence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def duration(self):
        return (self.end_date - self.start_date).days + 1

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='calendar_events')