from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

class Escuela(models.Model):
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

class User(AbstractUser):
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, null=True)
    edad = models.IntegerField(null=True)
    is_administrativo = models.BooleanField(default=False)
    is_profesor = models.BooleanField(default=False)
    is_estudiante = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Administrativo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Grupo(models.Model):
    escuela = models.ManyToManyField(Escuela)
    nombre = models.CharField(max_length=250)
    nivel = models.CharField(max_length=250)
