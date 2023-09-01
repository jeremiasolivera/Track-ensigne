from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.extract_faces, name='extracted'),
    path('pacientes/', views.patients_details, name='pacientes'),
    path('eliminar_paciente/<int:pk>', views.patients_delete, name='eliminar_paciente'),
    path('actualizar_paciente/<int:pk>', views.patients_update, name='actualizar_paciente'),
    path('recognition/', views.recognition, name='recognition'),
]
