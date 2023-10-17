from django.db import models

# Create your models here.
class Paciente(models.Model):

    estado_choices = (('En observacion', 'En observacion'), ('Atencion especial','Atencion especial'),
                      ('Alta medica', 'Alta medica'))


    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='pacientes/')
    edad = models.PositiveIntegerField()
    informe_medico = models.TextField()
    estado = models.CharField(max_length=20,choices=estado_choices, default='Alta medica')

    def __str__(self):
        return self.nombre