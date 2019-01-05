from django.urls import path
from salon.views import administrativo, estudiante, profesor

#app_name = 'salon'

urlpatterns = [
    path('signup/', administrativo.administrativoSignUpView.as_view(), name='signup'),
    
]
