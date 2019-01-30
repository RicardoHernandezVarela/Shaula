from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView

from salon.forms import EstudianteSignUpForm
from salon.models import User, Escuela, Administrativo, Profesor, Grupo, Curso, Seccion, Actividad, Estudiante
from salon.decorators import estudiante_required, admin_required

@method_decorator([login_required, admin_required], name='dispatch')
class estudianteSignUpView(CreateView):
    model = User
    form_class = EstudianteSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'estudiante'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
