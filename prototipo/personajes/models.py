from django.db import models
from django.contrib.auth.models import User

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    nivel = models.IntegerField(default=1)
    poder = models.CharField(max_length=100)
    equipo = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} ({self.owner.username})'
