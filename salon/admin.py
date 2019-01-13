from django.contrib import admin
from .models import User, Escuela, Grupo

admin.site.register(Escuela)
admin.site.register(User)
admin.site.register(Grupo)
