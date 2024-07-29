from django.shortcuts import render, redirect
from .models import Employee, Leave
from .forms import LeaveRequestForm

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'gestion_conges/employee_list.html', {'employees': employees})

def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
        form = LeaveRequestForm(request.POST, request.FILES)  # Ajoutez request.FILES pour les fichiers
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user  # Associe la demande de congé à l'utilisateur connecté
            leave_request.employee = Employee.objects.get(user=request.user)  # Associe la demande de congé à l'employé correspondant
            leave_request.save()
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()

    return render(request, 'gestion_conges/leave_request.html', {'form': form})
