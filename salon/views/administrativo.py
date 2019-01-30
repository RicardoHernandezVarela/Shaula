from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django import forms
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView

from salon.forms import AdministrativoSignUpForm, CursoForm, EstudianteForm
from salon.models import User, Escuela, Administrativo, Grupo, Curso, Profesor, Estudiante
from salon.decorators import admin_required

class administrativoSignUpView(CreateView):
    model = User
    form_class = AdministrativoSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administrativo'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('adminis:grupos')

@method_decorator([login_required, admin_required], name='dispatch')
class GruposView(ListView):
    model = Escuela
    template_name = 'salon/escuela.html'

    def get_queryset(self):
        queryset = self.request.user.escuela
        return queryset


@method_decorator([login_required, admin_required], name='dispatch')
class ProfesoresView(ListView):
    context_object_name = 'profesores'
    template_name = 'salon/profesores.html'

    def get_queryset(self):
        id = self.request.user.escuela.id
        usuarios = User.objects.filter(is_profesor=True)
        queryset = usuarios.filter(escuela_id=id)
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class AlumnosView(ListView):
    context_object_name = 'estudiantes'
    template_name = 'salon/alumnos.html'

    def get_queryset(self):
        id = self.request.user.escuela.id
        usuarios = User.objects.filter(is_estudiante=True)
        queryset = usuarios.filter(escuela_id=id)
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class CrearGrupo(CreateView):
    model = Grupo
    fields = ['nombre', 'nivel']
    template_name = 'salon/grupo_form.html'

    def form_valid(self, form):
        grupo = form.save(commit=False)
        grupo.escuela = self.request.user.escuela
        grupo.save()
        messages.success(self.request, 'Se creo el grupo con exito.')
        return redirect('adminis:grupos')

@method_decorator([login_required, admin_required], name='dispatch')
class CursosView(DetailView, FormView):
    model = Grupo
    template_name = 'salon/clases.html'
    form_class = EstudianteForm

    def get_object(self):
        grupo = Grupo.objects.get(pk=self.kwargs['pk'])
        return grupo

    def form_valid(self, form):
        grupo = Grupo.objects.get(pk=self.kwargs['pk'])
        estudiante = form.save(commit=False)
        estudiante.grupo = grupo
        estudiante.save()
        return redirect('adminis:cursos', grupo.pk)

@login_required
@admin_required
def crear_curso(request, pk):
    # Filtrar con el pk del curso y la escuela del usuario que crea el curso
    grupo = get_object_or_404(Grupo, pk=pk, escuela=request.user.escuela)

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.grupo = grupo
            curso.save()
            return redirect('adminis:cursos', grupo.pk)
    else:
        form = CursoForm()

    return render(request, 'salon/curso_form.html', {'grupo': grupo, 'form': form})
