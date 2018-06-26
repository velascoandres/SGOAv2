from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.objetos_aprendizaje.views import *


urlpatterns = [
	
	path('nuevo',oa_form_upload,name='oa_crear'),

	path('listar',oa_list,name='oa_listar'),
	path('editar/<pk>/',OA_Update.as_view(),name='oa_editar'),
    path('listar_ajax/',OA_List.as_view(),name='oa_listar_ajax'),
    path('eliminar/<pk>/',OA_Delete.as_view(),name='oa_eliminar'),
    path('vista/<int:id_oa>/',oa_vista,name='oa_ver'),
    path('descargar/<int:id_oa>/',OA_Download,name='oa_descargar'),
    path('crear_comentario/<int:id_oa>',comentario_form_upload,name='comentario_crear'),
    path('crear_comentario/<int:id_oa>/<int:id_cid>/',comentario_form_upload,name='subcomentario_crear'),
    path('comentarios/<int:id_oa>',listar_comentarios,name='co_listar'),
    path('busqueda',buscar,name='buscar'),
    path('busqueda_ajax/',BusquedaAjax.as_view(),name='buscar_ajax'),
    path('api/comentarios/',ComentarioAPI.as_view(),name="api"),
    path('comentarios2/<int:id_oa>',Comentarios,name='comentario2_crear')
] 
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""