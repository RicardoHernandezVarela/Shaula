from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from salon.forms import AdministrativoSignUpForm
from salon.models import User, Escuela, Administrativo
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
    #context_object_name = 'escuelas'
    template_name = 'salon/escuela.html'

    def get_queryset(self):
        queryset = self.request.user.escuela
        return queryset
