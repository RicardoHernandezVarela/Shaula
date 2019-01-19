from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from salon.forms import AdministrativoSignUpForm, ProfesorSignUpForm, SeccionForm
from salon.models import User, Escuela, Administrativo, Profesor, Grupo, Curso, Seccion
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

@login_required
@profesor_required
def ver_secciones(request, pk):
    # Filtrar con el pk del curso
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'salon/secciones_curso.html', {'curso': curso })

@login_required
@profesor_required
def crear_seccion(request, pk):
    # Filtrar con el pk del curso
    curso = get_object_or_404(Curso, pk=pk)

    if request.method == 'POST':
        form = SeccionForm(request.POST)
        if form.is_valid():
            seccion = form.save(commit=False)
            seccion.curso = curso
            seccion.save()
            return redirect('profesor:secciones', curso.pk)
    else:
        form = SeccionForm()
    return render(request, 'salon/seccion_form.html', {'curso': curso, 'form': form})

@login_required
@profesor_required
def ver_actividades(request, pk):
    # Filtrar con el pk de la Sección
    seccion = get_object_or_404(Seccion, pk=pk)
    return render(request, 'salon/actividades.html', {'seccion': seccion })
