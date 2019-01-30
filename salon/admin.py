from django.contrib import admin
from .models import User, Escuela, Grupo, Curso, Seccion, Actividad, Estudiante

admin.site.register(Escuela)
admin.site.register(User)
admin.site.register(Grupo)
admin.site.register(Curso)
admin.site.register(Seccion)
admin.site.register(Actividad)
admin.site.register(Estudiante)
