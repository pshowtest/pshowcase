from django import forms
from stdimage import StdImageField
from .models import Categoria, Herramienta, Perfil, Proyecto


#formularios de categoria
class categoria_edit_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('nombre_categoria',)


class categoria_delete_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ()


class categoria_create_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('nombre_categoria',)



 

#formulario de herramientas

class herramienta_edit_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ('nombre_herramienta',)


class herramienta_delete_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ()

class herramienta_create_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ('nombre_herramienta',)



#formulario de perfil

class perfil_edit_form(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('descripcion','alma_mater', 'carrera', )




#formulario de PROYECTO

class proyecto_create_form(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'reseña') 
        labels = {'nombre_proyecto':'Nombre'}
        widgets ={
            'nombre_proyecto': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Un nombre creativo para tu proyecto'
                }
            ),
            'reseña':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Agrega una breve descripcion de sobre que se trata tu proyecto'          
                }
            )
        }


class proyecto_edit_form(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'reseña')
