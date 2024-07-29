from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(null=True, blank=True, default=timezone.now)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other')
    address = models.TextField(null=True, blank=True, default='')
    phone_number = models.CharField(max_length=20, null=True, blank=True, default='')
    email = models.EmailField(unique=True, default='example@example.com')
    photo_url = models.CharField(max_length=255, null=True, blank=True, default='')
    department = models.CharField(max_length=100, default='Unassigned')

    def __str__(self):
        return self.email  # Changer pour 'self.email' ou 'self.first_name + " " + self.last_name' si 'user.username' n'est pas défini

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
    leave_type = models.CharField(max_length=100, default='vacances')
    type_of_leave = models.CharField(max_length=50, choices=TYPE_CHOICES, default='maladie')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    reason = models.TextField(blank=True, null=True, default='')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, default='')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    comments = models.TextField(blank=True, null=True, default='')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')

    def __str__(self):
        return f"{self.get_type_of_leave_display()} - {self.start_date} to {self.end_date}"
