from django.contrib import admin
from .models import User, Escuela, Administrativo

admin.site.register(Escuela)
admin.site.register(Administrativo)
admin.site.register(User)
