from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.html import escape, mark_safe
import datetime

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

    def __str__(self):
        return self.user.username

class Grupo(models.Model):
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=250)
    nivel = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre + ' - ' + self.nivel

class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' - ' + self.grupo.nombre + ' - ' + self.grupo.nivel

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cursos = models.ManyToManyField(Curso)

    def __str__(self):
        return self.user.username

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + str(self.grupo)

class Seccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.curso.nombre + ": Sección " + self.nombre

class Actividad(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField(default=datetime.date.today)
    puntaje = models.FloatField()

    CATEGORIAS = {
        ('examen','Examen'),
        ('tarea','Tarea'),
        ('ejclase','Ejercicios clase'),
        ('proyecto','Proyecto'),
        ('practica','Práctica'),
        ('extra','Extra')
    }

    categoria = models.CharField(choices=CATEGORIAS, max_length=50)

    class Meta:
        ordering = ['fecha'] #cambiar a id

    def __str__(self):
        return self.titulo


class SeccionesAlumno(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seccion) +  ' - ' + str(self.estudiante)

class Calificacion(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    seccionesalumno = models.ForeignKey(SeccionesAlumno, on_delete=models.CASCADE)
    puntos = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('profesor:actividades', kwargs={'pk': self.actividad.seccion.pk})

    def __str__(self):
        return str(self.actividad) + ' - ' + str(self.puntos)
