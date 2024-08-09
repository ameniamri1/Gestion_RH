# gestion_conges/views.py
from django.shortcuts import render
from .models import Employee, Leave
from .forms import LeaveRequestForm
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import  ApprovalLevel
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from .models import Absence
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, fields


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'gestion_conges/employee_list.html', {'employees': employees})

def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = Employee.objects.get(user=request.user)
            leave_request.save()
            return redirect('leave_list')  # Redirection après la soumission
    else:
        form = LeaveRequestForm()

    employees = Employee.objects.all()
    return render(request, 'gestion_conges/leave_request.html', {'form': form, 'employees': employees})

def leave_list(request):
    leaves = Leave.objects.all().select_related('employee', 'approved_by')  
    print(leaves) 
    return render(request, 'gestion_conges/leave_list.html', {'leaves': leaves})

def home(request):
    return render(request, 'gestion_conges/home.html')



def submit_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            try:
                # Associe l'employé à la demande de congé
                leave_request.employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                # Redirection en cas d'absence d'employé
                return redirect('error_page')  # Assurez-vous que 'error_page' existe et est configurée correctement
            
            leave_request.save()
            return redirect('leave_list')
        else:
            # Affiche les erreurs de formulaire en cas d'invalidité
            return render(request, 'gestion_conges/leave_request.html', {'form': form})
    else:
        form = LeaveRequestForm()

    # Affiche le formulaire pour une requête GET
    return render(request, 'gestion_conges/leave_request.html', {'form': form})

def send_notification(subject, message, recipient_list):
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list)

# La fonction notify_employee est redondante avec send_notification
def approve_leave_request(request, leave_id):
    leave_request = get_object_or_404(Leave, id=leave_id)
    if request.user not in leave_request.approved_by.all():
        current_approval_level = ApprovalLevel.objects.filter(approvers=request.user).first()
        if current_approval_level:
            leave_request.approved_by = request.user
            leave_request.approval_date = timezone.now()
            leave_request.status = 'approuvee'
            leave_request.save()

            # Passer au niveau suivant s'il y en a un
            next_approval_level = ApprovalLevel.objects.filter(level=current_approval_level.level + 1).first()
            if next_approval_level:
                next_approvers = next_approval_level.approvers.all()
                next_approvers_emails = [approver.email for approver in next_approvers]
                send_notification(
                    'Nouvelle demande de congé en attente d\'approbation',
                    f'Une demande de congé de {leave_request.employee} nécessite votre approbation.',
                    next_approvers_emails
                )
            else:
                leave_request.status = 'approuvee'
                leave_request.save()

            # Notification à l'employé
            send_notification(
                'Statut de votre demande de congé',
                f'Votre demande de congé du {leave_request.start_date} au {leave_request.end_date} a été approuvée.',
                [leave_request.employee.user.email]
            )

    return redirect('leave_list')


def notify_employee(leave_request):
    subject = 'Mise à jour de votre demande de congé'
    message = f'Votre demande de congé du {leave_request.start_date} au {leave_request.end_date} a été {leave_request.get_status_display()}.'
    recipient_list = [leave_request.employee.user.email]
    send_notification(subject, message, recipient_list)




def send_approval_notification(leave_request, approvers):
    subject = 'Nouvelle demande de congé en attente d\'approbation'
    message = f'Une nouvelle demande de congé de {leave_request.employee} nécessite votre approbation.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [approver.email for approver in approvers]
    
    send_mail(subject, message, from_email, recipient_list)

def pending_leave_requests(request):
    pending_leaves = Leave.objects.filter(status='en_attente')  # Filtre les demandes en attente
    return render(request, 'gestion_conges/pending_leave_requests.html', {'pending_leaves': pending_leaves})

def error_page(request):
    return render(request, 'gestion_conges/error_page.html')

def shared_calendar(request):
    # Récupérer tous les congés approuvés
    approved_leaves = Leave.objects.filter(status='approuvee')
    # Passer les congés au template
    return render(request, 'gestion_conges/shared_calendar.html', {'leaves': approved_leaves})




#tache 4
def absence_history(request):
    absences = Absence.objects.filter(employee__user=request.user)
    return render(request, 'gestion_conges/absence_history.html', {'absences': absences})



def absence_report(request):
    report_type = request.GET.get('report_type', 'employee')
    absences = Absence.objects.all()

    if report_type == 'department':
        absences = absences.values('employee__department').annotate(total_days=Sum('duration'))
    elif report_type == 'period':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        absences = absences.filter(start_date__gte=start_date, end_date__lte=end_date)

    return render(request, 'gestion_conges/absence_report.html', {'absences': absences})



def performance_indicators(request):
    total_days = 365  # Nombre de jours dans l'année
    absences = Absence.objects.filter(is_approved=True)

    # Calculer la durée des absences
    absences = absences.annotate(duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=fields.DurationField()))

    total_absent_days = absences.aggregate(total_days=Sum('duration'))['total_days'] or 0
    total_employees = Employee.objects.count()

    if total_employees > 0:
        absenteeism_rate = (total_absent_days / (total_days * total_employees)) * 100
    else:
        absenteeism_rate = 0

    return render(request, 'gestion_conges/performance_indicators.html', {'absenteeism_rate': absenteeism_rate, 'total_employees': total_employees, 'total_absent_days': total_absent_days})