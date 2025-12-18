from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout_view'),
    path('panel_jugador/', views.panel_jugador, name='panel_jugador'),
    path('panel_gm/', views.panel_gm, name='panel_gm'),
    path('crear_personaje/', views.create_character, name='create_character'),
    path('eliminar_personaje/<int:pk>/', views.eliminar_personaje, name='eliminar_personaje'),
    path('editar_personaje/<int:pk>/', views.editar_personaje, name='editar_personaje'),
]
