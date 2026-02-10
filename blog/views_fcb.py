from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comentario
from .forms import ComentarioForm, PostForm, RegistroUsuarioForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-fecha_publicacion')
    paginador= Paginator(post_list, 10) #10 posts por página
    numero_pagina =request.GET.get('page')
    posts = paginador.get_page(numero_pagina)
    
    return render(request, 'blog/index.html', {'posts': posts})

def detalle_post(request, slug): #post id para identificar el post que se quiere detallar
    #primero detallamos si el post existe caso contrario devuelve error
    post = get_object_or_404(Post, slug=slug) #si el objeto existe se captura dentro de la variable post
    comentarios = Comentario.objects.filter(post=post)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.save()
            return redirect('detalle_post', slug=post.slug)
    else:
        form = ComentarioForm()
    contexto = {'post': post, 'comentarios': comentarios, 'form': form}

    return render(request, 'blog/detalle_post.html', contexto)

@login_required
def eliminar_post(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect('index')
   
    return render(request, "blog/eliminar_post.html",{'post': post})   

@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html',{'form': form})

@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post_editado=form.save()
            return redirect('detalle_post', slug= post_editado.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/editar_post.html', {'form': form, 'post': post})

def buscar_posts(request):
    query = request.GET.get('q', '').strip() #si no hay nada en q devuelve cadena vacia. Strip elimina espacios vacios al inicio y final
    resultados = []
    if query:
        resultados = Post.objects.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)#filtro que combina la búsqueda de contenido y título (la | se usa para combinar)
            )
        
   
    return render(request, 'blog/buscar_posts.html', {'resultados': resultados, 'query': query})

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})
