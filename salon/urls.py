from django.urls import path, include
from django.views.generic.base import TemplateView
from salon.views import administrativo, estudiante, profesor

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('administrativo/', include(([
        path('', administrativo.GruposView.as_view(), name='grupos'),
    ], 'salon'), namespace='adminis')),

]
