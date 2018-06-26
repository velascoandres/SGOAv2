from django.urls import include
from django.urls import path
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index',index_usuario,name="index_usuario"),
    path('logout',LogoutView.as_view(), {'next_page':''},name='logout'),
    path('registrarEst',StudentSignUpView.as_view(),name='est_signup'),
    path('registrarPro',TeacherSignUpView.as_view(),name='pro_signup'),
    path('registro',SignUpView.as_view(),name='signup'),
    path('gestionPro',TeacherList.as_view(),name='gestionPro'),
    path('gestionEst',StudentList.as_view(),name='gestionEst'),
    path('login', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    path('mail/<int:id_usuario>/',ActivarCuenta,name='activar'),
    path('mail2/<int:id_usuario>/',DesactivarCuenta,name='desactivar'),
   
]

