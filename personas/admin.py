from django.contrib import admin

# Register your models here.

from .models import Usuario, Categoria, Herramienta, Segmento, Proyecto, Tipo_segmento, Tipo_permiso, Colaboracion, Perfil, Herramienta_proyecto

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Herramienta)

admin.site.register(Segmento)
admin.site.register(Proyecto)
admin.site.register(Tipo_segmento)

admin.site.register(Tipo_permiso)
admin.site.register(Colaboracion)
admin.site.register(Perfil)

admin.site.register(Herramienta_proyecto)