from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from apps.usuarios.models import *

# Create your models here.




class Categoria(models.Model):
	nombre_cate = models.CharField(max_length=20)
	
	def __str__(self):
		return '{}'.format(self.nombre_cate)

class Objeto_Aprendizaje(models.Model):
	nombre = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=50)
	fecha_creacion = models.DateField()
	#fzip=models.FileField(null=True, blank=True,upload_to='storage/',validators=[FileExtensionValidator(allowed_extensions=['zip'])],default='VACIO')
	fzip=models.FileField(upload_to="storage",null=True, blank=True,default='vacio.zip')
	#FK
	profesor=models.ForeignKey(Profesor,null=False,blank=False,on_delete=models.CASCADE)
	categoria = models.ForeignKey(Categoria,blank=False,null=False,on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.fzip)

class Comentario(models.Model):
	contenido = models.CharField(max_length=70)
	fecha_comentario=models.DateField()
	autor=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
	fimg=models.ImageField(upload_to="imgs",null=True, blank=True,default='')
	#FK
	objeto_aprendizaje = models.ForeignKey(Objeto_Aprendizaje,null=False,blank=False,on_delete=models.CASCADE)
	comentario=models.ForeignKey('self',on_delete=models.CASCADE,related_name="parent_comment",null=True,blank=True)