
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

app_name='personas'
urlpatterns = [
    path('',views.index, name='index'),
 
    path('logout', views.logout,  name='logout'),
    path('detalle_proyecto2/<int:id_proyecto>/', views.detalle_proyecto2, name='detalle_proyecto2'),
    path('listado_proyectos_usuario/<int:id_usuario>/', views.listado_proyectos_usuario, name='listado_proyectos_usuario'),
    path('busqueda_proyectos/', views.busqueda_proyectos, name='busqueda_proyectos'),
    path('ultimos_proyectos/', views.ultimos_proyectos, name='ultimos_proyectos'),
    path('resultado_busqueda_proyectos/', views.resultado_busqueda_proyectos, name='resultado_busqueda_proyectos'),
    path('busqueda_personas/', views.busqueda_personas, name='busqueda_personas'),
    path('ultimos_perfiles/', views.ultimos_perfiles, name='ultimos_perfiles'),
    path('resultado_busqueda_personas/', views.resultado_busqueda_personas, name='resultado_busqueda_personas'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('todos_proyectos/', views.todos_proyectos, name='todos_proyectos'),
    path('todas_personas/', views.todas_personas, name='todas_personas'),
    path('informar_problema/', views.informar_problema, name='informar_problema'),
  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)