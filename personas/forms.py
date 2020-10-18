from django import forms
from stdimage import StdImageField
from .models import Categoria, Herramienta, Perfil, Proyecto




#formularios de categoria
class categoria_edit_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('nombre_categoria',)
        labels= {'nombre_categoria':'Nombre'}
        widgets={
            'nombre_categoria': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: Edicion de imagen'
                }
            ),
        }


class categoria_delete_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ()


class categoria_create_form(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('nombre_categoria',)
        labels= {'nombre_categoria':'Nombre'}
        widgets={
            'nombre_categoria': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: Edicion de imagenes'
                }
            ),
        }



 

#formulario de herramientas

class herramienta_edit_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ('nombre_herramienta',)
        labels= {'nombre_herramienta':'Nombre'}
        widgets={
            'nombre_herramienta': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: Photoshop'
                }
            ),
        }

class herramienta_delete_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ()

class herramienta_create_form(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = ('nombre_herramienta',)
        labels= {'nombre_herramienta':'Nombre'}
        widgets={
            'nombre_herramienta': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: paint'
                }
            ),
        }


#formulario de perfil

class perfil_edit_form(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('descripcion','alma_mater', 'carrera', 'retrato' )        
        widgets ={
            'alma_mater': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: Hardvard '
                }
            ),
            'carrera': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'ej: Marketing'
                }
            ),
            'descripcion':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Cuenta algo interesante sobre ti mismo'          
                }
            )
        }



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
