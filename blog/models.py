from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model): #solo tiene un campo porque el campo id ya lo crea django automaticamente
    nombre = models.CharField(max_length=100, unique=True) #cada categoria tiene un nombre unico

    def __str__(self): #este metodo sirve para que cuando imprimamos el objeto nos muestre el nombre en vez de "Categoria object (1)"
        return self.nombre
    
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify # No olvides esta importación para el slug

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=500, help_text="Un pequeño avance para la portada")
    contenido = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE) 
    publicado = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # --- ESTILO MAGAZINE ---
    imagen = models.ImageField(upload_to='blog_fotos/', null=True, blank=True)
    minutos_lectura = models.IntegerField(default=5, help_text="Tiempo estimado de lectura")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            contador = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model): #relacion uno a muchos. Un comenario pertenece a un post, pero un post puede tener muchos comentarios
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios') #un comentario pertenece a un post. Si se borra el post se borran sus comentarios
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_usuario') #un autor puede tener muchos comentarios, pero un comentario solo pertenece a un autor. Si se borra el autor se borran sus comentarios
    texto = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True) #se crea automaticamente cuando se crea el comentario

    def __str__(self):
        return f'Comentario de {self.author.username} en {self.post.titulo}' #retorna el autor y el post al que pertenece el comentario cuando se imprime el objeto