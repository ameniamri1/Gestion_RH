#gestion_conges\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('leave-request/', views.leave_request, name='leave_request'),
    path('leave-list/', views.leave_list, name='leave_list'),
    path('submit-leave-request/', views.submit_leave_request, name='submit_leave_request'),
    path('approve-leave/<int:leave_id>/', views.approve_leave_request, name='approve_leave_request'),
    path('pending-leave-requests/', views.pending_leave_requests, name='pending_leave_requests'),
    path('error/', views.error_page, name='error_page'),  # Ajoutez cette ligne
    path('shared-calendar/', views.shared_calendar, name='shared_calendar'),  # Ajoutez cette ligne
    path('calendar/', views.calendar_view, name='calendar'),

]
