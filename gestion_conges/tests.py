from django.test import TestCase
from django.contrib.auth.models import User
from .models import Employee, Leave, ApprovalLevel

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='securepassword')
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            user=self.user
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.first_name, 'John')
        self.assertEqual(self.employee.last_name, 'Doe')
        self.assertEqual(self.employee.email, 'john.doe@example.com')
        self.assertEqual(self.employee.user, self.user)

    def test_employee_email_unique(self):
        with self.assertRaises(Exception):
            Employee.objects.create(
                first_name='Jane',
                last_name='Doe',
                email='john.doe@example.com',  # Duplicate email
                user=self.user
            )

class LeaveModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane_doe', password='securepassword')
        self.employee = Employee.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            user=self.user
        )
        self.leave = Leave.objects.create(
            employee=self.employee,
            leave_type='vacances',
            type_of_leave='vacances',
            start_date='2024-08-01',
            end_date='2024-08-10'
        )

    def test_leave_creation(self):
        self.assertEqual(self.leave.employee, self.employee)
        self.assertEqual(self.leave.leave_type, 'vacances')
        self.assertEqual(self.leave.start_date, '2024-08-01')
        self.assertEqual(self.leave.end_date, '2024-08-10')
        self.assertEqual(self.leave.status, 'en_attente')  # Default value

    def test_leave_status_update(self):
        self.leave.status = 'approuvee'
        self.leave.save()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, 'approuvee')

class ApprovalLevelModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='approver', password='securepassword')
        self.approval_level = ApprovalLevel.objects.create(
            name='Level 1',
            level=1
        )
        self.approval_level.approvers.add(self.user)

    def test_approval_level_creation(self):
        self.assertEqual(self.approval_level.name, 'Level 1')
        self.assertEqual(self.approval_level.level, 1)
        self.assertIn(self.user, self.approval_level.approvers.all())

class LeaveRequestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            user=self.user
        )
        self.leave = Leave.objects.create(
            employee=self.employee,
            leave_type='vacances',
            type_of_leave='vacances',
            start_date='2024-08-01',
            end_date='2024-08-10',
            status='en_attente'
        )

    def test_leave_request_creation(self):
        self.assertEqual(self.leave.status, 'en_attente')

    def test_leave_request_approval(self):
        self.leave.status = 'approuvee'
        self.leave.save()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, 'approuvee')

    def test_leave_request_rejection(self):
        self.leave.status = 'rejettee'
        self.leave.save()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, 'rejettee')

    def test_leave_request_attachment(self):
        self.leave.attachment = 'attachments/test_attachment.pdf'
        self.leave.save()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.attachment.name, 'attachments/test_attachment.pdf')

    def test_leave_request_approval_by_user(self):
        approver = User.objects.create_user(username='approver', password='approverpass')
        approval_level = ApprovalLevel.objects.create(
            name='Level 1',
            level=1
        )
        approval_level.approvers.add(approver)

        self.leave.approved_by = approver
        self.leave.save()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.approved_by, approver)
