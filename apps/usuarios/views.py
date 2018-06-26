from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from apps.usuarios.models import *
from apps.usuarios.forms import *
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views.generic import FormView, RedirectView
from django.contrib.auth.models import User
from django.views.generic import TemplateView,ListView


# Create your views here.
def index_usuario(request):
	return HttpResponse("Soy la pagina principal del sistema")


class SignUpView(TemplateView):
    template_name='registration/signup.html'


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def logout_us(request, *args, **kwargs):
    from django.utils import timezone
    user = request.user
    profile = user.get_profile()
    profile.last_logout = timezone.now()
    profile.save()
    logout(request, *args, **kwargs)

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Estudiante'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')




def ActivarCuenta(request,id_usuario):
    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    User = get_user_model()
    mensaje=User.objects.make_random_password()
    usuario=User.objects.get(id=id_usuario)
    email=usuario.email
    usuario.set_password(mensaje)
    usuario.is_active=True
    usuario.save()
    #email='velasco.andrs@gmail.com'
    send_mail('Clave', 'Estimado usuario su cuenta ha sido activada\n Clave: '+str(mensaje), 
        'objetosaprendizajeslibres@gmail.com', [str(email)], fail_silently=False)
    return redirect('usuarios:gestionPro')


def DesactivarCuenta(request,id_usuario):
    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    User = get_user_model()
    mensaje='Estimado usuario, su cuenta ha sido desactivada'
    usuario=User.objects.get(id=id_usuario)
    email=usuario.email
    usuario.set_password(User.objects.make_random_password())
    usuario.is_active=False
    usuario.save()
    #email='velasco.andrs@gmail.com'
    send_mail('CUENTA',str(mensaje), 
        'objetosaprendizajeslibres@gmail.com', [str(email)], fail_silently=False)
    return redirect('usuarios:gestionPro')    


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name='registration/signup_form.html'


    def get_context_data(self,**kwargs):
        kwargs['user_type'] = 'Profesor'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user = form.save()
        #login(self.request,user)
        return redirect('/')


class TeacherList(ListView):
    model = Profesor
    templade_name = 'usuarios/profesor_list.html'


class StudentList(ListView):
    model = Student
    templade_name = 'usuarios/student_list.html'



