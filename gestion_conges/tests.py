from django.test import TestCase
from .models import Leave, Employee
from django.contrib.auth.models import User

class LeaveModelTests(TestCase):
    def setUp(self):
        # Créer un utilisateur et un employé pour les tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            department='HR'
        )
        self.leave = Leave.objects.create(
            leave_type='vacances',
            type_of_leave='vacances',
            start_date='2024-07-01',
            end_date='2024-07-10',
            reason='Vacation',
            employee=self.user
        )

    def test_leave_creation(self):
        # Vérifier si le congé a été créé correctement
        self.assertEqual(self.leave.leave_type, 'vacances')
        self.assertEqual(self.leave.type_of_leave, 'vacances')
        self.assertEqual(self.leave.start_date, '2024-07-01')
        self.assertEqual(self.leave.end_date, '2024-07-10')
        self.assertEqual(self.leave.reason, 'Vacation')
