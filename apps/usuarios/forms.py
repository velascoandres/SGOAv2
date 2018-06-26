from django import forms
from apps.usuarios.models import *
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.db import transaction




class StudentSignUpForm(UserCreationForm):
	
	nombre=forms.CharField(label='Tu nombre', max_length=100)
	apellido=forms.CharField(label='Tu Apellido', max_length=100)
	email =forms.EmailField()
	facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

	class Meta(UserCreationForm.Meta):
		model = User
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_student = True
		user.email=self.cleaned_data.get('email')
		user.save()
		student = Student.objects.create(
			user=user,
			nombre=self.cleaned_data.get('nombre'),
			apellido=self.cleaned_data.get('apellido'),
			facultad=self.cleaned_data.get('facultad'))
		student.save()
		return user



class TeacherSignUpForm(forms.ModelForm):
	
	nombre=forms.CharField(label='Tu nombre', max_length=100)
	apellido=forms.CharField(label='Tu Apellido', max_length=100)
	email =forms.EmailField()
	cedula=forms.CharField(label='Tu Numero de Cedula', max_length=10)
	departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    
	class Meta(UserCreationForm.Meta):
		model = User
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_teacher = True
		user.is_active = False
		user.email=self.cleaned_data.get('email')
		user.set_password(User.objects.make_random_password())
		user.save()
		profesor = Profesor.objects.create(nombre=self.cleaned_data.get('nombre'),
			apellido=self.cleaned_data.get('apellido'),
			user=user,departamento=self.cleaned_data.get('departamento'),cedula=self.clean_cedula())
		profesor.save()
		return user

	def clean_cedula(self):
		ced = self.cleaned_data['cedula']
		msg = "La Cédula introducida no es válida"
		valores = [ int(ced[x]) * (2 - x % 2) for x in range(9) ]
		suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
		veri = 10 - (suma - (10 * (suma / 10)))
		if int(ced[9]) == int(str(veri)[-1:]):
			return ced
		else:
			return ced

"""
class UsuarioForm(forms.ModelForm):
	
	class Meta:	
		model = Usuario
		fields = [
			'username',
			'password',
			'tipo_usuario',
		]

		labels = {
			'username': 'Nombre' ,
			'tipo_usuario': 'Tipo de Usuario',
			'password': 'Clave',
			
		}

		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}) ,
			'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
			'password': forms.PasswordInput(),
			
		}


"""

"""
class ProfesorForm(forms.ModelForm):
	
	class Meta:	
		model = Profesor
		fields = [
			'nombre',
			'apellido',
			'numero_cedula',
			'email',
			'facultad',
			'departamento',
		]

		labels = {
			'nombre': 'Nombre' ,
			'apellido': 'Apellido',
			'numero_cedula': 'Cedula',
			'email':'Correo Electronico',
			'facultad':'Facultad',
			'departamento':'Departamento',
		}

		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}) ,
			'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
			'password': forms.PasswordInput(),
			
		}


class ProfesorForm(forms.ModelForm):
	
	class Meta:	
		model = Profesor
		fields = [
			'nombre',
			'password',
			'tipo_usuario',
		]

		labels = {
			'nombre': 'Nombre' ,
			'tipo_usuario': 'Tipo de Usuario',
			'password': 'Clave',
			
		}

		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}) ,
			'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
			'password': forms.PasswordInput(),
			
		}
"""


"""
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
"""