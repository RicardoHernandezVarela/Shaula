from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError

from salon.models import User, Escuela, Administrativo, Profesor, Estudiante, Grupo, Curso, Seccion, Actividad, Calificacion

class AdministrativoSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('escuela', 'username', 'first_name', 'last_name', 'email', 'edad')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_administrativo = True
        user.save()
        administrativo = Administrativo.objects.create(user=user)
        return user

class ProfesorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('escuela', 'username', 'first_name', 'last_name', 'email', 'edad')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_profesor = True
        user.save()
        profesor = Profesor.objects.create(user=user)
        return user

class EstudianteSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('escuela', 'username', 'first_name', 'last_name', 'email', 'edad')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_estudiante = True
        user.save()
        return user

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nombre',)

class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ('nombre',)

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ('titulo', 'puntaje', 'categoria')

class EstudianteForm(forms.ModelForm):
    id = 1 #Obtener este valor dinamicamente
    user = forms.ModelChoiceField(queryset=User.objects.filter(escuela_id=id, is_estudiante=True))

    class Meta:
        model = Estudiante
        fields = ('user',)

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ('seccionesalumno', 'puntos')
