from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comentario
from .forms import ComentarioForm, PostForm, RegistroUsuarioForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy 
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-fecha_publicacion']
    paginate_by = 10  # Número de posts por página

class BuscarPostsListView(ListView):
    model = Post
    template_name = "blog/buscar_posts.html"
    context_object_name = "resultados"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        resultados = []
        if query:
            resultados = self.model.objects.filter(
                Q(titulo__icontains=query) |
                Q(contenido__icontains=query)
            ).filter(publicado=True) 
        return resultados

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        return context


class DetallePostView(DetailView):
    model = Post
    template_name = "blog/detalle_post.html"
    context_object_name = "post"#sino especificamos context_object_name, el objeto se llamaria "object" 
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentarios"] = Comentario.objects.filter(post=self.object)
        context["form"] = ComentarioForm()
        return context
class ComentarioCreateView(LoginRequiredMixin,CreateView):
    model = Comentario
    form_class = ComentarioForm

    def form_valid(self, form):# creamos el comentario y lo asociamos al post correspondiente
        # 1. Capturamos el post al que pertenece el comentario
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=post_id)
        # 2. Creamos el objeto comentario pero sin guardarlo aún en la DB (commit=False)
        comentario = form.save(commit=False)
        # 3. ASIGNACIÓN AUTOMÁTICA DEL AUTOR (Esto toma al usuario que está logueado en la petición actual)
        comentario.author = self.request.user
        # 4. ASIGNACIÓN AUTOMÁTICA DEL POST AL QUE PERTENECE EL COMENTARIO
        comentario.post = post
        # 5. Guardamos el comentario en la DB
        comentario.save()
        return super().form_valid(form)

class PostMixinDetailView(DetailView, FormMixin):
    model = Post
    template_name = "blog/detalle_post.html"
    context_object_name = "post"
    form_class = ComentarioForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentarios"] = Comentario.objects.filter(post=self.object)
  
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comentario = form.save(commit=False)
        comentario.post = self.object
        comentario.save()
        return super().form_valid(form)
    def get_success_url(self):# redirige a la misma pagina del post despues de crear el comentario
        return reverse('detalle_post', kwargs={'slug': self.object.slug})

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/crear_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):#USERPASSMIXIN nos permite restringir el acceso a la vista solo al autor del post
    model = Post
    form_class = PostForm
    template_name = 'blog/editar_post.html'
    context_object_name = 'post'
    #vamos a controlar que quien esté editando el post sea el autor del mismo

    def get_success_url(self):
        return reverse('detalle_post', kwargs={'slug': self.object.slug})
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser #permitimos que el superusuario también pueda editar cualquier post
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = "blog/eliminar_post.html"
    context_object_name = "post"
    success_url = reverse_lazy("index")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser #permitimos que el superusuario también pueda eliminar cualquier post

class RegistroUsuarioCreateView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')


class MisPostsListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/mis_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-fecha_publicacion')