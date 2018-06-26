
from rest_framework.serializers import ModelSerializer
from apps.objetos_aprendizaje.models import Comentario



class ComentarioSerializer(ModelSerializer):
    class Meta:
        model= Comentario
        fields =('contenido','fecha_comentario','autor'
            ,'fimg','objeto_aprendizaje')

