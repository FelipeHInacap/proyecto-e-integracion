from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('profesional', 'Profesional'),
        ('administrador', 'Administrador'),
    ]
    
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username