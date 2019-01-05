from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError

from salon.models import User, Escuela, Administrativo

class AdministrativoSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'escuela', 'nombre', 'primer_apellido', 'segundo_apellido', 'edad')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_administrativo = True
        if commit:
            user.save()
        return user
