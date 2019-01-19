from django.contrib import admin
from .models import User, Escuela, Grupo, Curso

admin.site.register(Escuela)
admin.site.register(User)
admin.site.register(Grupo)
admin.site.register(Curso)
