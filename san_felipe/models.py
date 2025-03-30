from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.timezone import localtime, get_current_timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(default=now, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']  # Ordena productos alfabéticamente



class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        fecha_local = localtime(self.fecha_hora, get_current_timezone())
        fecha_formateada = fecha_local.strftime('%d de %B de %Y, %I:%M %p')
        return f"Pedido #{self.id} - {fecha_formateada} - ${self.total:,.2f}"

    def calcular_total(self):
        """Recalcula el total del pedido sumando los precios de los items."""
        self.total = sum(item.cantidad * item.precio_unitario for item in self.items.all())
        self.save()

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)  # Se guarda el nombre del producto
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, default=0.00)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.calcular_total()  # Recalcular total del pedido

    def __str__(self):
        return f"{self.cantidad} x {self.producto} - ${self.precio_unitario * self.cantidad:,.2f}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField(default=4)
    reservada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.numero} - Capacidad: {self.capacidad} - {'Reservada' if self.reservada else 'Disponible'}"


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha = models.DateField(default=now)
    hora = models.TimeField()
    mensaje = models.TextField(blank=True, null=True)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    creada = models.DateTimeField(default=now, null=True)

    def __str__(self):
        return f"Reserva de {self.nombre} - Mesa {self.mesa.numero}"

    class Meta:
        ordering = ['-fecha', '-hora']  # Últimas reservas primero