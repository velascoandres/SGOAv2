from rest_framework.views import APIView
from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,TemplateView
from django.urls import reverse_lazy
import json
from apps.objetos_aprendizaje.forms import *
from apps.objetos_aprendizaje.models import Objeto_Aprendizaje, Categoria,Comentario
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.objetos_aprendizaje.serializers import *


#Vista para descargar el oa
def OA_Download(request, id_oa):
	path=Objeto_Aprendizaje.objects.get(id=id_oa)
	file_path = os.path.join(settings.MEDIA_ROOT, str(path))
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/force-download")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404

#Metodo para descomprimir el zip
def unzip(name):
	import zipfile
	import shutil
	path_to_zip_file=settings.MEDIA_ROOT+"/"+str(name)
	shutil.rmtree('templates/TEMP/')
	os.makedirs('templates/TEMP/')
	directory_to_extract_to="templates/TEMP/"
	zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
	zip_ref.extractall(directory_to_extract_to)
	zip_ref.close()

#Vista para la pagina de inicio
def index_oa(request):
	return render(request,'TEMP/index.html')
	#return HttpResponseRedirect(settings.BASE_DIR+"/TEMP/index.html")

#Visualizar Objeto de aprendizaje
def oa_vista(request,id_oa):
	oa=Objeto_Aprendizaje.objects.get(id=id_oa)
	unzip(oa)
	return render(request,'TEMP/index.html')



def buscar(request):
	if request.method=='POST':
		form = BusquedaForm(request.POST)
		if form.is_valid():
			categoria=form.cleaned_data['categoria']
			print (str(categoria))
			oa=Objeto_Aprendizaje.objects.filter(categoria=categoria)
			contexto={'oas':oa}
			return render(request, 'objetos_aprendizaje/objeto_aprendizaje_list2.html',contexto)
	else:
		form=BusquedaForm()
	return render(request, 'objetos_aprendizaje/objeto_aprendizaje_form.html', {'form': form})


#Vista para crear oa y subir el zip
def oa_form_upload(request):
    if request.method == 'POST':
        form = Objeto_AprendizajeForm(request.POST, request.FILES)
        if form.is_valid():
        	oa=Objeto_Aprendizaje()
        	current_user = request.user
        	form.save(current_user)
        	return redirect('objetos_aprendizaje:oa_listar')
    else:
        form = Objeto_AprendizajeForm()
    return render(request, 'objetos_aprendizaje/objeto_aprendizaje_form.html', {'form': form})

#Vista para crear comentario

def comentario_form_upload(request,id_oa,id_cid=None):
	print ("El valor del id es: "+str(id_cid))
	if request.method == 'POST':

		# Si no es comentario del comentario preguntamos con el id que se envia
		if not id_cid:
			form = ComentarioForm(request.POST, request.FILES)
			if form.is_valid():
				comentario=Comentario()
				current_user = request.user
				form.save(current_user,id_oa)
				id=id_oa
				return redirect('objetos_aprendizaje:comentario_crear',id_oa=id_oa)

		form2 = SubComentarioForm(request.POST)
		if form2.is_valid():
			comentario=Comentario()
			current_user = request.user
			form2.save(current_user,id_oa,id_cid)
			print ("El valor del id es: "+str(id_cid))

			return redirect('objetos_aprendizaje:comentario_crear',id_oa=id_oa)
	else:
		form  = ComentarioForm()
		form2 = SubComentarioForm()
		comments_list=Comentario.objects.filter(objeto_aprendizaje__id=id_oa).order_by('fecha_comentario')
		paginator=Paginator(comments_list,50)
		page = request.GET.get('page')
		comments=paginator.get_page(page)
	return render(request, 'objetos_aprendizaje/comentario_form2.html', {'form': form,'comments':comments,'form2': form2})


#Listar los comentarios en base al objeto de aprendizaje
def listar_comentarios(request,id_oa):
	oa=Objeto_Aprendizaje.objects.get(id=id_oa)
	comments_list=Comentario.objects.filter(objeto_aprendizaje__id=id_oa)
	paginator=Paginator(comments_list,10)
	page = request.GET.get('page')
	comments=paginator.get_page(page)

	return render(request,'objetos_aprendizaje/comentario_list.html',{'oa':oa,'comments':comments})

#Listar objetos de aprendizaje
def oa_list(request):
	oas = Objeto_Aprendizaje.objects.all()
	contexto={'oas':oas}
	return render(request,'objetos_aprendizaje/objeto_aprendizaje_list2.html',contexto)


from django.core import serializers

#Busqueda de objetos de aprendizaje de forma dinamica
class BusquedaAjax(TemplateView):

	def get(self,request,*args,**kwargs):
		id_categoria=request.GET['id']
		oas=Objeto_Aprendizaje.objects.filter(categoria__id=id_categoria)
		print (oas)
		kwargs['oas']=oas

		data=serializers.serialize('json',oas,
			fields=('pk','nombre','descripcion','fecha_creacion','profesor','categoria'))

		return HttpResponse(data,content_type='application/json')

"""
def listarOa(request):
	if request.method=='POST':
		categoria_pk=request.POST['opciones']
		oa=Objects.get(categoria=categoria_pk)
		contexto={'oas':}
"""

"""
def oa_delete(request,id_oa):
	oa = Objeto_Aprendizaje.objects.get(id=id_oa)
	if request.method == 'POST':
		path_to_delete_file=settings.MEDIA_ROOT+"/"+str(oa)
		os.remove(path_to_delete_file)
		oa.delete()
		return redirect('objetos_aprendizaje:oa_listar')
	return render(request,'objetos_aprendizaje/objeto_aprendizaje_confirm_delete.html')
"""


#Esta vista es la que usa el ajax, envia las categorias para desplegarlas en un combo en el template
class OA_List(ListView):
	model = Categoria
	templade_name = 'objetos_aprendizaje/objeto_aprendizaje_list.html' #Este nombre hace referencia al templade categoria_list.html


#Vista obsoleta que se utilizaba para actualizar un objeto de aprendizaje
class OA_Update(UpdateView):
	model = Objeto_Aprendizaje
	form_class = Objeto_AprendizajeForm
	templade_name = 'objetos_aprendizaje/oa_form.html'
	success_url = reverse_lazy('objetos_aprendizaje:oa_listar')


#Vista para borrar un objeto de aprendizaje
class OA_Delete(DeleteView):
	model = Objeto_Aprendizaje
	templade_name = 'objetos_aprendizaje/oa_confirm_delete.html'
	success_url = reverse_lazy('objetos_aprendizaje:oa_listar')


# API de comentarios
class ComentarioAPI(APIView):

	def get(self,request,format=None):

		list=[]
		id_oa=request.GET['id']
		queryset=Comentario.objects.filter(objeto_aprendizaje__id=id_oa).order_by('-id')
		for row in queryset:
			list.append({'id':row.id,'contenido':row.contenido, 'fecha_comentario': str(row.fecha_comentario), 'autor': row.autor.username,'fimg':str(row.fimg),'objeto_aprendizaje':str(row.objeto_aprendizaje),'ida':str(row.autor.id)})
		paginate_by = 2
		comentario_list_json = json.dumps(list) #dump list as JSON

		return HttpResponse(comentario_list_json, content_type='application/json')

#Vista que renderiza el formulario para comentar un objeto de aprendizaje
def Comentarios(request,id_oa):
	if request.method == 'POST':
		form = ComentarioForm(request.POST)
		if form.is_valid():
			comentario=Comentario()
			current_user = request.user
			form.save(current_user,id_oa)
			return redirect('objetos_aprendizaje:comentario2_crear',id_oa=id_oa)
	else:
		form  = ComentarioForm()
	return render(request, 'objetos_aprendizaje/listar_comentarios.html', {'form': form,'id_oa':id_oa})


class Comentario_Delete(DeleteView):
	model = Comentario
	templade_name = 'objetos_aprendizaje/comentario_confirm_delete.html'
	success_url = reverse_lazy('objetos_aprendizaje:comentario2_crear')

def comentario_delete(request,id_co,id_oa):
	comentario = Comentario.objects.get(id=id_oa)
	if request.method == 'POST':
		comentario.delete()
		print ("El id del oa: "+str(id_oa))
		return redirect('objetos_aprendizaje:comentario2_crear',id_oa=id_co)
	return render(request,'objetos_aprendizaje/comentario_confirm_delete.html',{'ida':id_co})
