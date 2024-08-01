#gestion_rh\urls.py
"""gestion_rh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestion_conges import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Ajoutez cette ligne pour la page d'accueil
    path('gestion_conges/', include('gestion_conges.urls')),
    path('pending-leave-requests/', views.pending_leave_requests, name='pending_leave_requests'),
    path('pending-leave-requests/', views.submit_leave_request, name='pending_leave_requests'),

]
