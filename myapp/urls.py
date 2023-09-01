from django.urls import path, include
from . import views


urlpatterns = [
    path('pacientes/', views.patients_details, name='pacientes'),
    path('registrar_paciente', views.extract_faces, name='extracted'),
    path('eliminar_paciente/<int:pk>', views.patients_delete, name='eliminar_paciente'),
    path('actualizar_paciente/<int:pk>', views.patients_update, name='actualizar_paciente'),
    path('recognition/', views.recognition, name='recognition'),
]
