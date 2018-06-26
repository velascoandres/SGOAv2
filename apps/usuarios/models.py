from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.





class Facultad(models.Model):
	nombre_facultad=models.CharField(max_length=20)
	#color = models.CharField(max_length=7, default='#007bff')

	def __str__(self):
		return '{}'.format(self.nombre_facultad)

	def get_html_badge(self):
		name = escape(self.nombre_facultad)
		color = escape(self.color)
		html = '<span class="badge badge-primary" style="background-color: #007bff">%s</span>' % (nombre)
		return mark_safe(html)


class Departamento(models.Model):
	nombre_dep=models.CharField(max_length=20)
	
	def __str__(self):
		return '{}'.format(self.nombre_dep)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

 
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    facultad=models.ForeignKey(Facultad,null=False,blank=False,on_delete=models.CASCADE)

class Profesor(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	nombre=models.CharField(max_length=25)
	apellido=models.CharField(max_length=25)
	departamento=models.ForeignKey(Departamento,null=False,blank=False,on_delete=models.CASCADE)
	cedula=models.CharField(max_length=10,null=False,blank=False)

	def __str__(self):
		return '{}'.format(self.nombre)











"""
class Tipo_Usuario(models.Model):
	nombre_tip_usuario=models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(self.nombre_tip_usuario)


class Usuario(models.Model):
	username =models.CharField(max_length=20)
	password=models.CharField(max_length=30,null=True,blank=True,default='user')
	estado=models.BooleanField(default=True)
	#FK
	tipo_usuario=models.ForeignKey(Tipo_Usuario,null=False,blank=False,on_delete=models.CASCADE)

	
	def __str__(self):
		return '{}'.format(self.username)

class Facultad(models.Model):
	nombre_facultad=models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(self.nombre_facultad)


class Departamento(models.Model):
	nombre_dep=models.CharField(max_length=20)
	
	def __str__(self):
		return '{}'.format(self.nombre_dep)

class Profesor(models.Model):
	usuario= models.OneToOneField(User,on_delete=models.CASCADE)
	nombre=models.CharField(max_length=20)
	apellido=models.CharField(max_length=20)
	num_cedula=models.CharField(max_length=10)
	email=models.CharField(max_length=30)
	#FK
	departamento=models.ForeignKey(Departamento,null=False,blank=False,on_delete=models.CASCADE)
	facultad=models.ManyToManyField(Facultad,blank=False)

def create_profesor(sender, **kwargs):
    if kwargs['created']:
        profesor = Profesor.objects.create(user=kwargs['instance'])

post_save.connect(create_profesor, sender=User)

class Estudiante(models.Model):
	nombre=models.CharField(max_length=20)
	apellido=models.CharField(max_length=20)
	num_cedula=models.CharField(max_length=10)
	email=models.CharField(max_length=30)
	facultad=models.ForeignKey(Facultad,null=False,blank=False,on_delete=models.CASCADE)
"""