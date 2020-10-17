from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from personas.models import Usuario , Perfil, Proyecto, Colaboracion, Tipo_permiso, Segmento, Tipo_segmento
from personas.models import Herramienta_proyecto, Herramienta, Categoria
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login, authenticate
from stdimage import StdImageField
import os
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail



#from django.shortcuts import render_to_response


def recepcion_formulario(request):
    #modulo para captar formulario
    is_used=False

    if request.method == "POST":
        #categoria
        if request.POST.get('modelo') == 'categoria':
            is_used=True 
            #editar            
            if request.POST.get('operacion') =='editar':  
                id_aux = request.POST.get('categoria_id')
                categoria = Categoria.objects.get(id=id_aux)
                categoria.nombre_categoria =  request.POST.get('nombre_categoria')
                categoria.save()
                return redirect('/')

            if request.POST.get('operacion') =='borrar':                  
                id_aux = request.POST.get('categoria_id')
                cat_aux = Categoria.objects.get(id=id_aux)  
                cat_aux.delete()               
                return redirect('/')

            if request.POST.get('operacion') =='crear':                 
                nombre = request.POST.get('nombre_categoria')
                user_id = request.POST.get('id_usuario')
                user = Usuario.objects.get(id=user_id)
                Categoria.objects.create(nombre_categoria=nombre ,usuario= user )                                           
                return redirect('/')

        #herramienta
        if request.POST.get('modelo') == 'herramienta':   
            is_used=True         
            if request.POST.get('operacion') =='editar':                
                id_aux = request.POST.get('herramienta_id')
                herramienta = Herramienta.objects.get(id=id_aux)
                herramienta.nombre_herramienta =  request.POST.get('nombre_herramienta')
                herramienta.save()
                return redirect('/')

            if request.POST.get('operacion') =='borrar':  
                id_aux = request.POST.get('herramienta_id')
                herr_aux = Herramienta.objects.get(id=id_aux)  
                herr_aux.delete()               
                return redirect('/')

            if request.POST.get('operacion') =='crear':  
                nombre = request.POST.get('nombre_herramienta')       
                categoria_aux = Categoria.objects.get(id=request.POST.get('categoria'))                        
                Herramienta.objects.create(nombre_herramienta=nombre ,categoria=categoria_aux)  
                #return HttpResponse( categoria_aux.nombre_categoria)                                           
                return redirect('/')
        
        #perfil
        if request.POST.get('modelo') == 'perfil':            
            id_perfil = request.POST.get('id_perfil')
            perfil_aux = Perfil.objects.get(id=id_perfil)
            perfil_aux.descripcion =  request.POST.get('descripcion')
            perfil_aux.alma_mater =  request.POST.get('alma_mater')
            perfil_aux.carrera =  request.POST.get('carrera')
            perfil_aux.save()
            HttpResponse('flag')
            return redirect('/') 

        #proyectos
        if request.POST.get('modelo') == 'proyecto':
            if request.POST.get('operacion') =='crear':     
                is_used=True            
                usuario_aux = Usuario.objects.get(id= request.POST.get('id_usuario'))
                pro_aux = Proyecto.objects.create(
                    nombre_proyecto=request.POST.get('nombre_proyecto'),
                    reseña=request.POST.get('reseña'),
                    fecha_creacion=datetime.now() 
                    )
                tipo_permiso_aux = Tipo_permiso.objects.get(nombre_permiso="propietario")
                colaboracion = Colaboracion.objects.create(
                    usuario = usuario_aux, 
                    tipo_permiso= tipo_permiso_aux, 
                    proyecto=pro_aux, 
                    fecha_colaboracion=datetime.now()
                    )  
                return redirect('detalle_proyecto2/'+str(pro_aux.id))                       


        #iniciar sesion
        if request.POST.get('modelo') == 'sesion':   
            is_used=True                   
            username=request.POST.get('usuario')
            password=request.POST.get('contraseña')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    return is_used

def index(request):
    recepcion_formulario(request)
    return render(request, 'personas/inicio.html')


def detalle_proyecto2(request, id_proyecto):  
    recepcion_formulario(request)  
    
    proyecto_aux2 = Proyecto.objects.get(id=id_proyecto)
    lista_segmentos = list()
    tipos_segmentos = Tipo_segmento.objects.all()
    # obtener todos los segmentos en los cuales esta ese proyecto
    segmentos = Segmento.objects.filter(proyecto=proyecto_aux2).order_by('numero_segmento')
    for s in segmentos:
        segm_aux = s
        lista_segmentos.append(s)
    
    
    if request.POST.get('modelo') == 'proyecto':
        if request.POST.get('operacion') =='borrar':
            proy_aux= Proyecto.objects.get(id=request.POST.get('id_proyecto') )
            proy_aux.delete()  
            return redirect('/')

        if request.POST.get('operacion') =='editar':
            proy_aux= Proyecto.objects.get(id=request.POST.get('id_proyecto') )
            proy_aux.nombre_proyecto = request.POST.get('nombre_proyecto')
            proy_aux.reseña = request.POST.get('reseña')
            proy_aux.save()  
            return redirect('/')

    if request.POST.get('modelo') == 'colaboracion':
        if request.POST.get('operacion') =='agregar':                   
            id_permiso = request.POST.get('tipo_permiso')
            id_proyecto = request.POST.get('id_proyecto')
            usuario=request.POST.get('usuario')
            tip_permiso_aux= Tipo_permiso.objects.get(id=id_permiso)
            proyecto_aux = Proyecto.objects.get(id=id_proyecto)
            usuario_aux= Usuario.objects.get(id=usuario)
            colab_aux= Colaboracion.objects.create(usuario=usuario_aux, tipo_permiso=tip_permiso_aux, proyecto=proyecto_aux, fecha_colaboracion=datetime.now()  )
            return redirect('/')

        if request.POST.get('operacion') =='borrar':                
            id_proyecto = request.POST.get('id_proyecto')
            usuario=request.POST.get('colaborador')
            proyecto_aux = Proyecto.objects.get(id=id_proyecto)
            usuario_aux= Usuario.objects.get(id=usuario)

            colab_aux= Colaboracion.objects.get(usuario=usuario_aux, proyecto=proyecto_aux )     
            colab_aux.delete()          
            return redirect('/')
            
        if request.POST.get('operacion') =='editar':                
            id_proyecto = request.POST.get('id_proyecto')
            usuario=request.POST.get('colaborador')
            proyecto_aux = Proyecto.objects.get(id=id_proyecto)
            usuario_aux= Usuario.objects.get(id=usuario)
            permiso = Tipo_permiso.objects.get(id= request.POST.get('permiso'))
            colab_aux= Colaboracion.objects.get(usuario=usuario_aux, proyecto=proyecto_aux )    
            colab_aux.tipo_permiso =permiso
            colab_aux.save()          
            return redirect('/')

    if request.POST.get('modelo') == 'herramientaProyecto':
        if request.POST.get('operacion') =='agregar':
            herramienta_aux = Herramienta.objects.get(id= request.POST.get('herramienta_id'))
            proyecto_aux = Proyecto.objects.get(id=request.POST.get('id_proyecto'))

            if Herramienta_proyecto.objects.filter(herramienta=herramienta_aux, proyecto=proyecto_aux ).exists():
                var='no pasa nada'
            else:
                Herramienta_proyecto.objects.create(herramienta=herramienta_aux, proyecto=proyecto_aux ) 
                

        if request.POST.get('operacion') =='borrar':
                id_herr =  request.POST.get('herramienta_id')
                id_proy = request.POST.get('id_proyecto')
                herramienta_aux = Herramienta.objects.get(id=id_herr)
                proyecto_aux = Proyecto.objects.get(id=id_proy)

                herr_pro_aux = Herramienta_proyecto.objects.get(herramienta=herramienta_aux, proyecto=proyecto_aux )
                herr_pro_aux.delete()

    if request.POST.get('modelo') == 'segmento':    
        if request.POST.get('operacion') =='crear':  
            proy_aux= Proyecto.objects.get(id=request.POST.get('id_proyecto') )

            #para determinar numero de segmento
            num_segmentos= Segmento.objects.filter(proyecto=proy_aux).count()

            # tipo texto 
            if request.POST.get('tipo_segmento')=='texto':
                tipo_segmento_aux = Tipo_segmento.objects.get(nombre_segmento='texto')
                nuevo_segmento= Segmento.objects.create(
                    proyecto=proy_aux,
                    numero_segmento= (num_segmentos+1),
                    tipo_segmento =tipo_segmento_aux ,
                    fecha_date = datetime.now(),
                    titular = request.POST.get('titular'),
                    var1= request.POST.get('descripcion')                   
                )
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )

            # tipo video 
            if request.POST.get('tipo_segmento')=='video':
                tipo_segmento_aux = Tipo_segmento.objects.get(nombre_segmento='video')
                link_editado =  request.POST.get('link').replace('https://youtu.be/','' )
                nuevo_segmento= Segmento.objects.create(
                    proyecto=proy_aux,
                    numero_segmento= (num_segmentos+1),
                    tipo_segmento =tipo_segmento_aux ,
                    fecha_date = datetime.now(),
                    titular = request.POST.get('titular'),
                    var1= request.POST.get('descripcion'),
                    var2=link_editado           
                )
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )

            # tipo codigo 
            if request.POST.get('tipo_segmento')=='codigo':
                tipo_segmento_aux = Tipo_segmento.objects.get(nombre_segmento='codigo')              
                nuevo_segmento= Segmento.objects.create(
                    proyecto=proy_aux,
                    numero_segmento= (num_segmentos+1),
                    tipo_segmento =tipo_segmento_aux ,
                    fecha_date = datetime.now(),
                    titular = request.POST.get('titular'),
                    var1= request.POST.get('descripcion'),
                    var2=request.POST.get('link')          
                )
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )
            
            # tipo archivo 
            if request.POST.get('tipo_segmento')=='archivo':
                tipo_segmento_aux = Tipo_segmento.objects.get(nombre_segmento='archivo')              
                nuevo_segmento= Segmento.objects.create(
                    proyecto=proy_aux,
                    numero_segmento= (num_segmentos+1),
                    tipo_segmento =tipo_segmento_aux ,
                    fecha_date = datetime.now(),
                    titular = request.POST.get('titular'),
                    var1= request.POST.get('descripcion'),
                    var2=request.POST.get('link')          
                )
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )


            # tipo imagen 
            if request.POST.get('tipo_segmento')=='imagen':
                tipo_segmento_aux = Tipo_segmento.objects.get(nombre_segmento='imagen')              
                nuevo_segmento= Segmento.objects.create(
                    proyecto=proy_aux,
                    numero_segmento= (num_segmentos+1),
                    tipo_segmento =tipo_segmento_aux ,
                    fecha_date = datetime.now(),
                    titular = request.POST.get('titular'),
                    var1= request.POST.get('descripcion'),
                    var2=request.POST.get('link')          
                )
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )


        if request.POST.get('operacion') =='editar':        
            if request.POST.get('tipo_segmento')=='texto':               
                segmento_aux= Segmento.objects.get(id=request.POST.get('id_segmento'))                                                                                                                       
                segmento_aux.titular = request.POST.get('titular')
                segmento_aux.var1= request.POST.get('descripcion')             
                segmento_aux.save()                
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )

            if request.POST.get('tipo_segmento')=='video':  
                link_editado =  request.POST.get('link').replace('https://youtu.be/','' )             
                segmento_aux= Segmento.objects.get(id=request.POST.get('id_segmento'))                                                                                                                       
                segmento_aux.titular = request.POST.get('titular')
                segmento_aux.var1= request.POST.get('descripcion')   
                segmento_aux.var2= link_editado           
                segmento_aux.save()                
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )
                
            if request.POST.get('tipo_segmento')=='archivo':               
                segmento_aux= Segmento.objects.get(id=request.POST.get('id_segmento'))                                                                                                                       
                segmento_aux.titular = request.POST.get('titular')
                segmento_aux.var1= request.POST.get('descripcion')   
                segmento_aux.var2= request.POST.get('link')            
                segmento_aux.save()                
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )
                
            if request.POST.get('tipo_segmento')=='codigo':               
                segmento_aux= Segmento.objects.get(id=request.POST.get('id_segmento'))                                                                                                                       
                segmento_aux.titular = request.POST.get('titular')
                segmento_aux.var1= request.POST.get('descripcion')   
                segmento_aux.var2= request.POST.get('link')            
                segmento_aux.save()                
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )

            if request.POST.get('tipo_segmento')=='imagen':               
                segmento_aux= Segmento.objects.get(id=request.POST.get('id_segmento'))                                                                                                                       
                segmento_aux.titular = request.POST.get('titular')
                segmento_aux.var1= request.POST.get('descripcion')   
                segmento_aux.var2= request.POST.get('link')            
                segmento_aux.save()                
                return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )

        if request.POST.get('operacion') =='borrar':
            proy_aux= Proyecto.objects.get(id=request.POST.get('id_proyecto') )
            seg_aux= Segmento.objects.get(id=request.POST.get('id_segmento')) 
            seg_aux.delete()
            lista_segmentos = Segmento.objects.filter(proyecto=proy_aux ).order_by('numero_segmento')   
            contador=1                     
            for ls in lista_segmentos:
                seg_aux2= Segmento.objects.get(id=ls.id)
                seg_aux2.numero_segmento = contador
                seg_aux2.save()
                contador=contador+1

            return redirect('/detalle_proyecto2/'+str(request.POST.get('id_proyecto')) )
            

   
    proyecto_aux = Proyecto.objects.get(id=id_proyecto)
    permisos = Tipo_permiso.objects.all()
    listado_colaboradores = list()
    listado_no_colaboradores= list()
    usuarios_colaboraciones = list()
    listado_herramienta_proyecto = list()
    listado_herr_pro = list()
    listado_herramientas=list()

    colaboradores = Colaboracion.objects.filter(proyecto=proyecto_aux)
    for c in colaboradores:
        listado_colaboradores.append(c)
        user_aux = Usuario.objects.get(id= c.usuario.id)
        usuarios_colaboraciones.append(user_aux)

    todo_usuarios=Usuario.objects.all()
    for tu in todo_usuarios:
        existencia = False
        for u in usuarios_colaboraciones:
            if u == tu:                
                existencia=True
        if existencia==False:
            listado_no_colaboradores.append(tu)


    herramientas_proyectos = Herramienta_proyecto.objects.filter(proyecto=proyecto_aux)
    for hp in herramientas_proyectos:
        listado_herr_pro.append(hp)
        herr = Herramienta.objects.get(id= hp.herramienta.id)
        listado_herramientas.append(herr)

   
    context={'proyecto_aux':proyecto_aux , 
    'listado_herr_pro':listado_herr_pro , 'listado_herramientas':listado_herramientas , 'usuarios_colaboraciones':usuarios_colaboraciones, 
    'listado_colaboradores':listado_colaboradores, 'permisos':permisos ,'listado_no_colaboradores':listado_no_colaboradores,  'lista_segmentos':lista_segmentos,
        'tipos_segmentos':tipos_segmentos,
        'proyecto_aux2':proyecto_aux2, }
    return render(request, 'personas/detalle_proyecto.html',context)


def logout(request):
        #modulo para captar formulario
    if request.method == "POST":
        # si es un formulario de categoria 
        if request.POST.get('tipo_form') == 'categoria':
            prueba = request.POST.get('categoria_id')
            categoria = Categoria.objects.get(id=prueba)
            categoria.nombre_categoria =  request.POST.get('nombre_categoria')
            categoria.save()
            return redirect('/')

        #si es un formulario de herramienta 
        if request.POST.get('tipo_form') == 'herramienta':
            prueba = request.POST.get('herramienta_id')
            herramienta = Herramienta.objects.get(id=prueba)
            herramienta.nombre_herramienta =  request.POST.get('nombre_herramienta')
            herramienta.save()
            return redirect('/')


        #si es un formulario de perfil
        if request.POST.get('tipo_form') == 'perfil':
            prueba = request.POST.get('perfil_id')
            perfil = Perfil.objects.get(id=prueba)
            perfil.descripcion =  request.POST.get('descripcion')
            perfil.alma_mater =  request.POST.get('alma_mater')
            perfil.carrera =  request.POST.get('carrera')
            perfil.save()
            return redirect('/')                   
    #fin de modulo

    # Redireccionamos a la portada
    do_logout(request)
    return redirect('/')


def busqueda_personas(request):
    recepcion_formulario(request)
    return render(request, 'personas/busqueda_personas.html')     

    
def busqueda_proyectos(request):
    recepcion_formulario(request)
    return render(request, 'personas/busqueda_proyectos.html')  
   

def crear_cuenta(request):
    #no deberia poder crear cuenta estando logeado
    if request.method == "POST":
        user_aux = User.objects.create_user(
            username= request.POST.get('user_name') ,
            email = request.POST.get('correo') ,
            password= request.POST.get('password') ,         
        )

        username_aux = request.POST.get('user_name') 
        password_aux = request.POST.get('password')
        usuario_aux = Usuario.objects.create(
            id_usuario =  request.POST.get('rut') ,
            user_credentials = user_aux,
            dv = request.POST.get('dv') ,
            nombre1 = request.POST.get('nombre1') ,
            nombre2 = request.POST.get('nombre2') ,
            apellido1 = request.POST.get('apellido1') ,
            apellido2 = request.POST.get('apellido2') ,
            correo = request.POST.get('correo') ,
            fecha_nacimiento = request.POST.get('fecha_nacimiento') ,            
        )

        perfil_aux = Perfil.objects.create(
            alma_mater = "algun lugar",
            carrera = "algo",
            descripcion = "descripcion",
            usuario= usuario_aux,
            fecha_creacion= datetime.now()
        )

     
        #userfinal=authenticate(username=username_aux, password=password_aux)
        #do_login(request, userfinal)
        return redirect('/')

    return render(request, 'personas/crear_cuenta.html' )


#recibe como parametro un listado de proyectos
def listar_proyectos(request, lista_proyectos, titulo):    
    lista_herramientas = list()
    lista_categorias = list()
    lista_colaboraciones = list()
    lista_herram_proy = list()
    #lista donde en cada elemento, primer valor es id del proyecto, segundop valor es n° de colaboradores
    #y el tercer valor es el numero de segmntos de cada priyecto
    tupla_datos=list()

    for p in lista_proyectos:
        #determino listado de colaboraciones que tengan a ese proyecto
        colab_aux = Colaboracion.objects.filter(proyecto=p)
        for c in colab_aux:            
            lista_colaboraciones.append(c)
        num_colaboraciones =  Colaboracion.objects.filter(proyecto=p).count()
        num_segmentos = Segmento.objects.filter(proyecto=p).count()
        tupla_datos.append([p, num_colaboraciones, num_segmentos])

        #determino las herramienta- proyecto
        herr_pro_aux = Herramienta_proyecto.objects.filter(proyecto=p)
        for hp in herr_pro_aux:            
            lista_herram_proy.append(hp)
            #guardo a la vez las herramientas 
            herr_aux= Herramienta.objects.get(id=hp.herramienta.id)
            lista_herramientas.append(herr_aux)
            #guardo a la vez las categorias 
            categoria_aux = Categoria.objects.get(id=herr_aux.categoria.id)
            lista_categorias.append(categoria_aux)

        #determino la cantidad de segmentos 
        
        lista_herramientas= list(set(lista_herramientas))
        lista_categorias= list(set(lista_categorias))
        lista_colaboraciones= list(set(lista_colaboraciones))



    #genero las variables que voy a utilizar 
    context ={
        'lista_proyectos':lista_proyectos ,
        'lista_herramientas':lista_herramientas, 
        'lista_categorias':lista_categorias,
        'lista_colaboraciones':lista_colaboraciones,
        'lista_herram_proy':lista_herram_proy,
        'tupla_datos':tupla_datos,
        'titulo':titulo
     
    }
    return render(request, 'personas/listar_proyectos.html', context )


def todos_proyectos(request):
    recepcion_formulario(request)
    proyectos_parametro = Proyecto.objects.all()
    titulo='Mostrando todos los proyectos'
    return listar_proyectos(request, proyectos_parametro, titulo)


def ultimos_proyectos(request):
    recepcion_formulario(request)
    ultimos_proyectos = Proyecto.objects.order_by('-fecha_creacion')[:5]
    titulo='Ultimos proyectos añadidos'
    return listar_proyectos(request,ultimos_proyectos ,titulo)


def listado_proyectos_usuario(request, id_usuario):
    recepcion_formulario(request)
    #buscar los proyectos en los que participa ese usuario
    user = Usuario.objects.get(id=id_usuario)
    #todas las colaboraciones de ese usuario
    listado_colaboraciones= Colaboracion.objects.filter(usuario=id_usuario)    
    listado_proyectos=list()

    for lc in listado_colaboraciones:
        proy_aux = Proyecto.objects.get(id=lc.proyecto.id)  
        listado_proyectos.append(proy_aux)      
    titulo=('Proyectos en los que "%s" participa' %(user.nombre1 +' '+ user.apellido1))
    return listar_proyectos(request,listado_proyectos,titulo )


def ultimos_perfiles(request):
    recepcion_formulario(request)
    ultimos_perfiles = Perfil.objects.order_by('-fecha_creacion')[:5]
    ultimos_usuarios = list()    

    for i in ultimos_perfiles:
        user_aux = Usuario.objects.get(id_usuario=i.usuario.id_usuario)        
        ultimos_usuarios.append(user_aux)  
              
    titulo ='Mostrando ultimos perfiles creados'
    
    return listar_personas(request,ultimos_usuarios, titulo )


#recibe como parametro una lista de usuarios
def listar_personas(request, lista_usuarios, titulo):   
    lista_perfiles = list()    
    tupla_datos=list()
      
    for u in lista_usuarios:
        perfil_aux = Perfil.objects.get(usuario= u)
        lista_perfiles.append(perfil_aux)
        colaboraciones_usuario =  Colaboracion.objects.filter(usuario=u)
        num_colaboraciones_totales= colaboraciones_usuario.count()
        #determino las colaboraciones de usuario que son propietario
        tipo_permiso_aux = Tipo_permiso.objects.get(nombre_permiso= 'propietario')
        contador_proyectos_subidos=0  
        for cu in colaboraciones_usuario:
            if cu.tipo_permiso == tipo_permiso_aux:
                contador_proyectos_subidos= contador_proyectos_subidos +1
        colaboraciones= num_colaboraciones_totales- contador_proyectos_subidos
        #se envia el usuario, los proyectos prpietarios, las colaboraciones por cada usuario
        tupla_datos.append([u , contador_proyectos_subidos, colaboraciones])

    #genero las variables que voy a utilizar 
    context ={
        'lista_usuarios':lista_usuarios,
        'lista_perfiles':lista_perfiles ,
        'tupla_datos':tupla_datos, 
        'titulo':titulo            
    }
    return render(request, 'personas/listar_personas.html', context )


def todas_personas(request):
    recepcion_formulario(request)
    lista_personas = Usuario.objects.all()
    titulo='Mostrando todas los usuarios creados'
    return listar_personas(request, lista_personas, titulo)


def resultado_busqueda_personas(request):
    if recepcion_formulario(request) != False: 
        return redirect('/resultado_busqueda_personas')
    #recepcion_formulario(request)    
    if request.method == "POST":
        if request.POST.get('operacion') == 'busqueda':            
            cadena_minusculas= (request.POST.get('texto_busqueda')).lower()
            cadena_truncada = cadena_minusculas.split()
           
            usuarios_coincidentes=list()
            #revisar en los nombres y apellidos de usuario
            usuarios_todos = Usuario.objects.all()
            for u in usuarios_todos:
                for c in cadena_truncada:  
                    nombre1 = u.nombre1.lower()
                    nombre2 = u.nombre2.lower()
                    apellido1= u.apellido1.lower()
                    apellido2= u.apellido2.lower()
                    correo = u.correo.lower()
                    if ((nombre1.find(c)!= -1)or(nombre2.find(c)!=-1)or(apellido1.find(c)!=-1)or(apellido2.find(c)!=-1)or(correo.find(c)!=-1)):
                        usuarios_coincidentes.append(u)
            titulo = 'Mostrando resultado de "%s"' %request.POST.get('texto_busqueda')
            
            usuarios_coincidentes = list(set(usuarios_coincidentes))
            return listar_personas(request,usuarios_coincidentes,titulo )
    else:
        return redirect('/')


def resultado_busqueda_proyectos(request):  
    if recepcion_formulario(request) != False: 
        return redirect('/resultado_busqueda_proyectos')
    recepcion_formulario(request)
    if request.method == "POST":
        cadena_minusculas= (request.POST.get('texto_busqueda')).lower()
        cadena_truncada = cadena_minusculas.split()
        proyectos_coincidentes=list()       
        proyect_herramienta=list()
                     
        #revisar titulos de proyectos
        todo_proyectos= Proyecto.objects.all()
        
        for tp in todo_proyectos:
            coincidencia=False
            titulo= tp.nombre_proyecto.lower()
            #busco si algo del texto ingresado coincide con algo del nombre del proyecto
            for ct in cadena_truncada:         
                if titulo.find(ct) != -1:
                    coincidencia=True
            #si algo coincidio agrego el proyecto al listado
            if coincidencia==True:
                proyectos_coincidentes.append(tp)
            #si nada coincidio sigo buscando por las herramientas del proyecto
            else:
                #obtengo las herramientas asociadas a ese proyecto
                herr_pro_aux= Herramienta_proyecto.objects.filter(proyecto=tp)
                
                #busco cada herramienta alguna coincidencia
                for hpx in herr_pro_aux:
                    #obtengo el nombre de la herramienta 
                    herramienta_aux= Herramienta.objects.get(id=hpx.herramienta.id)
                    nombre_herramienta = herramienta_aux.nombre_herramienta.lower()
                    coincidencia=False
                    #comparo el nombre con la cadena ingresada
                    for ct in cadena_truncada:         
                        if nombre_herramienta.find(ct) != -1:
                            coincidencia=True
                    
                    if coincidencia==True:
                        proyectos_coincidentes.append(tp)
                    else:
                        #busco en la categoria asociada a esa herrameinta
                        cat_aux= Categoria.objects.get(id=herramienta_aux.categoria.id)
                        nombre_categoria = cat_aux.nombre_categoria.lower()
                        coincidencia=False
                        for ct in cadena_truncada:         
                            if nombre_categoria.find(ct) != -1:
                                coincidencia=True

                        if coincidencia==True:
                            proyectos_coincidentes.append(tp)

                    
            
        proyectos_coincidentes= list(set(proyectos_coincidentes))    
        titulo='Resultados de busqueda por " %s "' % request.POST.get('texto_busqueda')
        return listar_proyectos(request, proyectos_coincidentes, titulo )
    else:
        return redirect('/')

def informar_problema(request):
    if request.method == "POST":
        if request.POST.get('operacion') == 'enviar_correo':
            emisor = request.POST.get('correo')
            receptor = list()
            receptor.append('pshowcase.contacto@gmail.com')
            asunto = request.POST.get('asunto') 
            cuerpo = 'consulta realizada por usuario: '+emisor + '\n'+ request.POST.get('descripcion')
           
            #se envia confirmacion
            emisor2 = request.POST.get('correo')
            receptor2 = list()
            receptor2.append(emisor2)
            asunto2 = 'recepcion de problema o sugerencia'
            cuerpo2 = 'Hola, hemos recibido un correo con asunto: '+ asunto +' , muchas gracias , tu correo sera leido y respondido a la brevedad'
            

            send_mail( asunto , cuerpo, emisor,
            receptor, fail_silently=False)

            send_mail( asunto2 , cuerpo2, emisor2,
            receptor2, fail_silently=False)


            #email_message.send()

    return render(request, 'personas/enviar_correo.html')
 
