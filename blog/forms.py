#importamos el modelo
from .models import Comentario, Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#modelForms
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [ 'texto']
        
        widgets = {
            
            'texto': forms.Textarea(attrs={'class':'form-control mb-2', 'rows':3, 'placeholder':'Ingresa tu comentario'})
        }   
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria', 'publicado']
        error_messages = {
            'titulo': {
                'max_length': 'El título no puede tener más de 100 caracteres',
                'required': 'El campo título es obligatorio'
            },
            'contenido': {
                'required': 'El campo contenido es obligatorio'
            },
            'categoria': {
                'required': 'El campo categoría es obligatorio'
            }
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Ingresa el título del post'}),
            'contenido': forms.Textarea(attrs={'class':'form-control mb-2', 'rows':5, 'placeholder':'Ingresa el contenido del post'}),
            # Select es el menú desplegable para elegir la categoría
            'categoria': forms.Select(attrs={'class':'form-control mb-2'}),
            # CheckboxInput es la casilla de verificación
            'publicado': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 
                  'first_name', 
                  'last_name', 
                  'email', 
                  'password1', 
                  'password2'
                  )
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           placeholders = {
               'username': 'Ingrese su nombre de usuario',
               'first_name': 'Ingrese su nombre',
               'last_name': 'Ingrese su apellido',
               'email': 'Ingrese su correo',
                'password1': 'Ingrese su contraseña',
                'password2': 'Repita su contraseña'
           }
           for name, field in self.fields.items():
               field.widget.attrs.update({
                   'class': 'form-control mb-2',
                   'placeholder': placeholders.get(name, '')
               })