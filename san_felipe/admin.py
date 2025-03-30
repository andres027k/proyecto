from django.contrib import admin
from .models import Producto, Mesa, Pedido, ItemPedido, PerfilUsuario, Reserva

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible')
    list_editable = ('disponible',)  # Permite cambiar disponibilidad directamente

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacidad')  # Puedes agregar más campos si quieres

admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(PerfilUsuario)
admin.site.register(Reserva)


