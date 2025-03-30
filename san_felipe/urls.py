from django.urls import path
from . import views
from django.contrib import admin
from .views import enviar_pedido, confirmar_pedido
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import sugerencias
from .views import nosotros_view
from .views import enviar_reserva, mesas_disponibles
from .views import enviar_sugerencia
from .views import historial_pedidos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('enviar-sugerencia/', enviar_sugerencia, name='enviar_sugerencia'),
    path("confirmar-pedido/", confirmar_pedido, name="confirmar_pedido"),
    path('', views.index, name='index'),
    path('tienda/', views.tienda, name='tienda'),
    path('reservar/', views.reservar, name='reservar'),
    path('manual/', views.manual, name='manual'),
    path("enviar-reserva/", enviar_reserva, name="enviar_reserva"),
    path("mesas-disponibles/", mesas_disponibles, name="mesas_disponibles"),
    path('pedido/', views.pedido, name='pedido'),
    path("enviar-pedido/", enviar_pedido, name="enviar_pedido"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.logout_view, name='logout'),  
    path("sugerencias/", sugerencias, name="sugerencia"),
    path("nosotros/", nosotros_view, name="nosotros"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('historial/', historial_pedidos, name='historial_pedidos'),
    path('recuperar/', views.recuperar, name='recuperar'),
     path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)