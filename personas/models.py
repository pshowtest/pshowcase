from django.db import models
from django.utils import timezone 
from stdimage import StdImageField
from django.contrib.auth.models import User

class Usuario(models.Model):
    def __str__(self):
        return str(self.id)
    id_usuario = models.IntegerField(default=0, unique=True)
    user_credentials = models.OneToOneField(User, on_delete=models.CASCADE)
    dv= models.CharField(max_length=200)
    nombre1 = models.CharField(max_length=200)
    nombre2 = models.CharField(max_length=200)
    apellido1 = models.CharField(max_length=200)
    apellido2 = models.CharField(max_length=200)
    correo = models.CharField(max_length=200, unique=True)
    fecha_nacimiento = models.DateTimeField()


class Categoria(models.Model):
    def __str__(self):
        return str(self.id)

    #id_categoria = IntegerField(default=0)
    nombre_categoria = models.CharField(max_length=200)
    usuario  = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    icono_categoria = models.CharField(max_length=200)


class Herramienta(models.Model):
    def __str__(self):
        return str(self.id)

    #id_herramienta = IntegerField(default=0)
    nombre_herramienta = models.CharField(max_length=200)
    categoria  = models.ForeignKey(Categoria, on_delete=models.CASCADE)
   


class Proyecto(models.Model):
    def __str__(self):
        return str(self.id)

    #id_proyecto = IntegerField(default=0)
    nombre_proyecto = models.CharField(max_length=200)
    reseña = models.CharField(max_length=500,null=True, blank=True )
    fecha_creacion = models.DateTimeField()



class Tipo_segmento(models.Model):  
    def __str__(self):
        return str(self.id)
    #id_tipo_segmento = IntegerField(default=0)
    nombre_segmento = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)



class Segmento(models.Model):
    def __str__(self):        
        return str(self.id)
    #id_segmento = IntegerField(default=0)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    numero_segmento =models.IntegerField(default=0)
    tipo_segmento  = models.ForeignKey(Tipo_segmento, on_delete=models.CASCADE)
    fecha_date = models.DateTimeField()
    titular = models.CharField(max_length=200, null=True, blank=True)
    #se usaran estas variables para definir los diferentes tipos de segmentos
    var1 =  models.CharField(max_length=1000, null=True, blank=True)
    var2 =  models.CharField(max_length=1000, null=True, blank=True)
    var3 =  models.CharField(max_length=1000, null=True, blank=True)
    var4 =  models.CharField(max_length=1000, null=True, blank=True)
    var5 =  models.CharField(max_length=1000, null=True, blank=True)



class Tipo_permiso(models.Model):
    def __str__(self):
        return self.nombre_permiso
    #id_tipo_permiso  = IntegerField(default=0)
    nombre_permiso = models.CharField(max_length=200)
    descripcion_tipo_permiso = models.CharField(max_length=200)




class Colaboracion(models.Model):
    def __str__(self):       
        return str(self.id)
    #id_colaboracion = IntegerField(default=0)
    #me guarda el id del models usuario, no el id_usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_permiso = models.ForeignKey(Tipo_permiso, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_colaboracion = models.DateTimeField()



class Perfil(models.Model):
    def __str__(self):      
        return str(self.id)
    usuario =  models.ForeignKey(Usuario, on_delete=models.CASCADE,unique=True )
    descripcion =  models.CharField(max_length=200 ,null=True)
    alma_mater = models.CharField(max_length=200,null=True)
    carrera = models.CharField(max_length=200,null=True)
    retrato = StdImageField(upload_to='avatar/' , null=True, blank=True, variations={'thumbnail': (100, 100, True)})
    #retrato = models.ImageField(null=True, blank=True)
    fecha_creacion = models.DateTimeField()



class Herramienta_proyecto(models.Model):
    def __str__(self):
        return str(self.id)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE )
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE )


















