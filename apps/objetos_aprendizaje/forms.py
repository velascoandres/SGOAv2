from django import forms
from apps.objetos_aprendizaje.models import Objeto_Aprendizaje,Categoria,Comentario
from apps.usuarios.models import Profesor
import time

class Objeto_AprendizajeForm(forms.ModelForm):
	
	class Meta:	
		model = Objeto_Aprendizaje
		fields = [
			'nombre',
			'descripcion',
			'fecha_creacion',
			'fzip',
			'categoria'
		]

		labels = {
			'nombre': 'Nombre' ,
			'descripcion': 'Descripcion',
			'fecha_creacion': 'Fecha de creacion',
			'fzip':'Archivo Zip',
			'categoria':'Categorias',
		}

		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}) ,
			'descripcion': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_creacion': forms.TextInput(attrs={'class':'form-control'}),
			#'fzip':forms.FileField(),
			'categoria': forms.Select(attrs={'class':'form-control'}),
		}

	def save(self,c_user):
		oa = super().save(commit=False)
		profesor = Profesor.objects.get(user=c_user)
		oa = Objeto_Aprendizaje.objects.create(nombre=self.cleaned_data.get('nombre'),descripcion=self.cleaned_data.get('descripcion'),profesor=profesor,fzip=self.cleaned_data.get('fzip'),categoria=self.cleaned_data.get('categoria'),fecha_creacion=self.cleaned_data.get('fecha_creacion'))
		oa.save()
		return oa



class BusquedaForm(forms.Form):
	categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)


class ComentarioForm(forms.ModelForm):
	
	class Meta:	
		model = Comentario
		fields = [
			'contenido',
			'fimg',
		]

		labels = {
			'contenido': 'Respuesta' ,
			'fimg':'Imagen',
		}

		widgets = {
			'contenido': forms.TextInput(attrs={'class':'form-control'}),
		}

	def save(self,c_user,c_oa):
		comentario = super().save(commit=False)
		from django.contrib.auth import get_user_model
		User = get_user_model()
		fecha=str(time.strftime("%Y-%m-%d"))
		usuario = User.objects.get(id=c_user.id)
		oa=Objeto_Aprendizaje.objects.get(id=c_oa)
		comentario = Comentario.objects.create(contenido=self.cleaned_data.get('contenido')
			,fecha_comentario=fecha,
			autor=usuario,fimg=self.cleaned_data.get('fimg'),objeto_aprendizaje=oa)
		comentario.save()
		return comentario


class SubComentarioForm(forms.ModelForm):


	class Meta:	
		model = Comentario
		fields = [
			'contenido',
			'id',
		]

		labels = {
			'contenido': 'Respuesta' ,
		}

		widgets = {
			'contenido': forms.TextInput(attrs={'class':'form-control'}),
		}

	def save(self,c_user,c_oa,id_cid):
		comentario = super().save(commit=False)
		from django.contrib.auth import get_user_model
		User = get_user_model()
		fecha=str(time.strftime("%Y-%m-%d"))
		usuario = User.objects.get(id=c_user.id)
		oa=Objeto_Aprendizaje.objects.get(id=c_oa)
		com=Comentario.objects.get(id=id_cid)
		comentario = Comentario.objects.create(contenido=self.cleaned_data.get('contenido')
			,fecha_comentario=fecha,
			autor=usuario,fimg='Ninguna',objeto_aprendizaje=oa,comentario=com)
		comentario.save()
		return comentario
	
	
