from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError

from salon.models import User, Escuela, Administrativo, Profesor, Grupo, Curso, Seccion

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
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('escuela', 'username', 'first_name', 'last_name', 'email', 'edad')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_profesor = True
        user.save()
        profesor = Profesor.objects.create(user=user)
        profesor.cursos.add(*self.cleaned_data.get('cursos'))
        return user

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nombre',)

class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ('nombre',)
