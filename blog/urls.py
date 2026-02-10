from django.urls import path
from .views import MisPostsListView, PostListView, BuscarPostsListView,DetallePostView, ComentarioCreateView, PostCreateView, PostUpdateView,PostDeleteView, PostMixinDetailView, RegistroUsuarioCreateView, MisPostsListView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/buscar/', BuscarPostsListView.as_view(), name='buscar_posts'),
   # path('post/<int:id>', DetallePostView.as_view(), name='detalle_post'),
    #path("post/<int:post_id>/comentar", ComentarioCreateView.as_view(), name="crear_comentario"),
    path('post/<slug:slug>/', PostMixinDetailView.as_view(), name='detalle_post'),
    path('post/crear', PostCreateView.as_view(), name='crear_post'),
    path('post/<slug:slug>/editar/', PostUpdateView.as_view(), name='editar_post'),
    path("post/<slug:slug>/eliminar", PostDeleteView.as_view(), name="eliminar_post"),
    path('registro/', RegistroUsuarioCreateView.as_view(), name='registro'),
    path('mis_posts/', MisPostsListView.as_view(), name='mis_posts'),
    
    
]
