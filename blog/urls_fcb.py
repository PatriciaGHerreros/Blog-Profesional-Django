from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/buscar/', views.buscar_posts, name='buscar_posts'),
    path('post/crear', views.crear_post, name='crear_post'),
    path('registro/', views.registro_usuario, name='registro'),
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('post/<slug:slug>/editar/', views.editar_post, name='editar_post'),
    path("post/<slug:slug>/eliminar", views.eliminar_post, name="eliminar_post"),
   
    
    
    
]
