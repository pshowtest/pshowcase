from stdimage import StdImageField
from personas.models import Usuario , Perfil, Proyecto, Colaboracion, Tipo_permiso, Segmento, Tipo_segmento
from personas.models import Herramienta_proyecto, Herramienta, Categoria
from  .forms import  categoria_edit_form, herramienta_edit_form, perfil_edit_form, categoria_create_form, categoria_delete_form, herramienta_delete_form
from  .forms import herramienta_create_form ,proyecto_create_form, proyecto_edit_form
from django.contrib.auth.models import User


 #actualizacion del contexto processor
def datos_usuario(request):
    #se generan errores cuando uno de los campos no se haya y levanta excepcion
    try:
        usuario_conectado =  Usuario.objects.get(user_credentials=request.user)
        categorias_usuario = Categoria.objects.filter(usuario = usuario_conectado)
        perfil_usuario = Perfil.objects.get(usuario=usuario_conectado)
        colaboraciones_usuario = Colaboracion.objects.filter(usuario=usuario_conectado)
        proyectos_usuario = list()
        herramientas_usuario = list()

        for c in categorias_usuario:
            herramientas_aux = Herramienta.objects.filter(categoria=c)
            for h in herramientas_aux:
                herramientas_usuario.append(h)

        for cl in colaboraciones_usuario:
            id_pr= cl.proyecto.id
            proyecto_aux = Proyecto.objects.get(id=cl.proyecto.id)
            proyectos_usuario.append(proyecto_aux)



        return {'usuario_conectado':usuario_conectado, 'categorias_usuario':categorias_usuario, 'herramientas_usuario':herramientas_usuario, 
        'perfil_usuario':perfil_usuario, 'colaboraciones_usuario':colaboraciones_usuario, 'proyectos_usuario':proyectos_usuario }
    except:
        return{}



def formularios(request):

    form_create_categoria = categoria_create_form()
    form_delete_categoria= categoria_delete_form()
    form_edit_categorias = categoria_edit_form()

    form_delete_herramienta= herramienta_delete_form()
    form_create_herramienta=  herramienta_create_form()
    form_edit_herramientas = herramienta_edit_form()

    form_edit_perfil = perfil_edit_form()

    form_create_proyecto= proyecto_create_form()
    form_edit_proyecto = proyecto_edit_form()

    return {'form_edit_categorias':form_edit_categorias, 'form_edit_herramientas':form_edit_herramientas,
    'form_edit_perfil':form_edit_perfil , 'form_create_categoria':form_create_categoria , 'form_delete_categoria':form_delete_categoria,
    'form_delete_herramienta':form_delete_herramienta, 'form_create_herramienta':form_create_herramienta ,
    'form_create_proyecto':form_create_proyecto, 'form_edit_proyecto':form_edit_proyecto }








   