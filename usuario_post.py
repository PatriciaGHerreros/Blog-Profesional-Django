import os
import django
import random
import requests
from django.core.files import File
from tempfile import NamedTemporaryFile
from faker import Faker

# 1. Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_profesional.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comentario, Categoria

fake = Faker('es_ES')

def unificar_datos():
    print("🧹 Limpiando base de datos para evitar duplicados...")
    Post.objects.all().delete()
    # Comentario.objects.all().delete() # Se borran solos al borrar los posts
    
    # --- PASO 1: CREAR USUARIOS (Tu lógica de creacion_usuarios) ---
    print("👤 Creando usuarios...")
    usuarios = []
    NUM_USERS = 5 # He bajado el número para que no tarde tanto
    for _ in range(NUM_USERS):
        username = fake.user_name()
        while User.objects.filter(username=username).exists():
            username = fake.user_name()
        
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        usuarios.append(user)
    print(f"✅ {len(usuarios)} usuarios listos.")

    # --- PASO 2: CREAR CATEGORIAS (Tu lógica de ingresar_datos) ---
    print("📂 Creando categorías...")
    categorias_lista = ["Programación", "Ciberseguridad", "Redes", "Desarrollo Web", "Inteligencia Artificial", "Fotografía"]
    categorias_objetos = []
    for nombre in categorias_lista:
        cat, created = Categoria.objects.get_or_create(nombre=nombre)
        categorias_objetos.append(cat)

    # --- PASO 3: CREAR POSTS CON IMÁGENES Y COMENTARIOS ---
    print("📝 Creando posts con imágenes (estética Magazine)...")
    NUM_POSTS = 15 # Cantidad ideal para el examen
    
    for i in range(NUM_POSTS):
        categoria = random.choice(categorias_objetos)
        autor = random.choice(usuarios)
        
        # Creamos la instancia del post
        post = Post(
            titulo=fake.sentence(nb_words=6).replace(".", ""),
            resumen=fake.paragraph(nb_sentences=3), # CAMPO NUEVO
            contenido=fake.paragraph(nb_sentences=15),
            categoria=categoria,
            author=autor,
            publicado=True,
            minutos_lectura=random.randint(3, 12) # CAMPO NUEVO
        )

        # Lógica de descarga de imagen (Imprescindible para el estilo visual)
        try:
            url_imagen = "https://loremflickr.com/800/500/minimal,nature/all"
            response = requests.get(url_imagen, timeout=10)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                post.imagen.save(f"post_{i}.jpg", File(img_temp), save=False) # save=False porque lo guardamos abajo
        except:
            print(f"⚠️ No se pudo descargar imagen para el post {i+1}")

        post.save()

        # --- PASO 4: COMENTARIOS (Tu lógica de ingresar_datos) ---
        num_comentarios = random.randint(2, 4)
        for _ in range(num_comentarios):
            # Seleccionamos un usuario real de nuestra lista para que sea el autor
            autor_comentario = random.choice(usuarios) 
            
            Comentario.objects.create(
                post=post,
                author=autor_comentario,  # <--- Ahora le pasamos el objeto Usuario
                texto=fake.text(max_nb_chars=200)
                # fecha_comentario se pone sola por el auto_now_add=True
            )
        print(f"🚀 Post {i+1}/{NUM_POSTS} creado con éxito.")

    print("\n✨ ¡Proceso finalizado! Base de datos poblada y estética.")

if __name__ == '__main__':
    unificar_datos()