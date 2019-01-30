from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView

from salon.forms import ProfesorSignUpForm, SeccionForm, ActividadForm, CalificacionForm
from salon.models import User, Escuela, Administrativo, Profesor, Grupo, Curso, Seccion, Actividad, SeccionesAlumno, Calificacion
from salon.decorators import profesor_required, admin_required

@method_decorator([login_required, admin_required], name='dispatch')
class profesorSignUpView(CreateView):
    model = User
    form_class = ProfesorSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'profesor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

@method_decorator([login_required, profesor_required], name='dispatch')
class ProfesorBoard(ListView):
    context_object_name = 'cursos'
    template_name = 'salon/profesor_board.html'

    def get_queryset(self):
        queryset = self.request.user.profesor.cursos.all()
        return queryset

# Ver secciones (unidades) y crear nuevas secciones
@method_decorator([login_required, profesor_required], name='dispatch')
class ver_secciones(DetailView, FormView):
    template_name = 'salon/secciones_curso.html'
    model = Curso
    form_class = SeccionForm

    def get_object(self):
        curso = Curso.objects.get(pk=self.kwargs['pk'])
        return curso

    def form_valid(self, form):
        curso = Curso.objects.get(pk=self.kwargs['pk'])
        grupo = curso.grupo
        seccion = form.save(commit=False)
        seccion.curso = curso
        seccion.save()
        for estudiante in grupo.estudiante_set.all():
            SeccionesAlumno.objects.create(seccion=seccion, estudiante=estudiante)
        return redirect('profesor:secciones', curso.pk)

@method_decorator([login_required, profesor_required], name='dispatch')
class ver_actividades(DetailView, FormView):
    template_name = 'salon/actividades.html'
    model = Seccion
    form_class = ActividadForm

    def get_object(self):
        seccion = Seccion.objects.get(pk=self.kwargs['pk'])
        return seccion

    def form_valid(self, form):
        seccion = Seccion.objects.get(pk=self.kwargs['pk'])
        seccionesalumno = seccion.seccionesalumno_set.all()
        actividad = form.save(commit=False)
        actividad.seccion = seccion
        actividad.save()
        for sec_alum in seccionesalumno:
            Calificacion.objects.create(actividad=actividad, seccionesalumno=sec_alum, puntos=1)
        return redirect('profesor:actividades', seccion.pk)

@method_decorator([login_required, profesor_required], name='dispatch')
class calificar(UpdateView):
    model = Calificacion
    fields = ['puntos']

@login_required
@profesor_required
def calificar_actividad(request, pk):
    # Filtrar con el pk del curso y la escuela del usuario que crea el curso
    actividad = get_object_or_404(Actividad, pk=pk)

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.actividad = actividad
            calificacion.save()
            return redirect('profesor:actividades', actividad.seccion.pk)
    else:
        form = CalificacionForm()

    return render(request, 'salon/calificacion_form.html', {'actividad': actividad, 'form': form})
