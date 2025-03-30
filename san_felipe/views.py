from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from .models import PerfilUsuario, Producto, Pedido, Mesa, Reserva
from django.shortcuts import render
from .forms import SugerenciaForm, ReservaForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, LoginView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Pedido, ItemPedido
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Pedido, ItemPedido, Producto

def enviar_sugerencia(request):
    if request.method == 'POST':
        data = request.POST
        nombre = data.get('nombre')
        email = data.get('email')
        sugerencia = data.get('sugerencia')

        # Enviar correo
        send_mail(
            subject=f'Sugerencia de {nombre}',
            message=f'Nombre: {nombre}\nCorreo: {email}\nSugerencia: {sugerencia}',
            from_email='soportesanfelipe324@gmail.com',
            recipient_list=['andresbustos170@gmail.com'],
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def mesas_disponibles(request):
    """Retorna la lista de mesas que no están reservadas para la fecha y hora actual."""
    reservas_activas = Reserva.objects.filter(fecha=now().date(), hora__gte=now().time()).values_list("mesa_id", flat=True)
    mesas_libres = Mesa.objects.exclude(id__in=reservas_activas)

    # Convertir las mesas en una lista de diccionarios
    data = [{"id": mesa.id, "numero": mesa.numero} for mesa in mesas_libres]

    return JsonResponse({"mesas": data})

def enviar_reserva(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Verificar si la mesa ya está reservada en la misma fecha y hora
        existe_reserva = Reserva.objects.filter(
            mesa__numero=data["mesa"], fecha=data["fecha"], hora=data["hora"]
        ).exists()

        if existe_reserva:
            return JsonResponse({"error": "Esta mesa ya ha sido reservada."}, status=400)

        # Guardar la reserva
        mesa = Mesa.objects.get(numero=data["mesa"])
        nueva_reserva = Reserva.objects.create(
            nombre=data["nombre"],
            email=data["email"],
            telefono=data["telefono"],
            fecha=data["fecha"],
            hora=data["hora"],
            mensaje=data["mensaje"],
            mesa=mesa
        )

        # Enviar correo
        mensaje_correo = f"""
        Nueva reserva realizada:
        Nombre: {nueva_reserva.nombre}
        Email: {nueva_reserva.email}
        Teléfono: {nueva_reserva.telefono}
        Fecha: {nueva_reserva.fecha}
        Hora: {nueva_reserva.hora}
        Mesa: {nueva_reserva.mesa.numero}
        Mensaje: {nueva_reserva.mensaje}
        """

        send_mail(
            "Nueva Reserva Recibida",
            mensaje_correo,
            "tuemail@gmail.com",
            ["andresbustos170@gmail.com"],
            fail_silently=False,
        )

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Método no permitido"}, status=400)

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.success(request, f"Bienvenido, {request.user.username} (Admin)!")
            return redirect("/admin/")  
        messages.success(request, f"Bienvenido de nuevo, {request.user.username}!")
        return redirect("/pedido/")  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Por favor, ingresa ambos campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")

            if user.is_superuser:
                return redirect("/admin/")  
            return redirect("/pedido/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        telefono = request.POST.get("telefono")
        direccion = request.POST.get("direccion")

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            user_existente = User.objects.get(username=username)
            # Si el usuario es superusuario, evitar registro
            if user_existente.is_superuser:
                messages.error(request, "No puedes registrarte como administrador desde aquí.")
                return redirect("register")
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect("register")

        # Crear el usuario normal (no admin)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Crear perfil de usuario solo si NO es superusuario
        if not user.is_superuser:
            PerfilUsuario.objects.create(user=user, telefono=telefono, direccion=direccion)

        # Iniciar sesión automáticamente
        auth_login(request, user)
        messages.success(request, "Registro exitoso.")

        return redirect("/pedido/")  # ✅ Redirige al pedido

    return render(request, "register.html")


@csrf_exempt
@login_required
def enviar_pedido(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pedido_items = data.get("pedido", [])
            metodo_pago = data.get("metodo_pago", "No especificado")

            if not pedido_items:
                return JsonResponse({"mensaje": "El pedido está vacío"}, status=400)

            usuario = request.user
            nuevo_pedido = Pedido.objects.create(usuario=usuario)

            total = 0
            pedido_detalle = []  # Para el cuerpo del correo

            for item in pedido_items:
                subtotal = item["cantidad"] * item["precio"]
                total += subtotal
                ItemPedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=item["nombre"],
                    cantidad=item["cantidad"],
                    precio_unitario=item["precio"]
                )
                pedido_detalle.append(f"  - {item['nombre']} (x{item['cantidad']}) → ${subtotal}")

            # Guardar el total en el pedido
            nuevo_pedido.total = total
            nuevo_pedido.save()

            # Formatear el detalle del pedido
            pedido_texto = "\n".join(pedido_detalle)

            # 📩 Correo para el Usuario
            mensaje_usuario = f"""
            Hola {usuario.first_name},

            🎉 ¡Tu pedido en San Felipe está confirmado!

            Aquí tienes los detalles:
            ___________________________
            {pedido_texto}
            ___________________________

            💰 Total: ${total}
            💳 Método de pago: {metodo_pago}

            📲 **Envía tu comprobante de pago:**
            🌐 *Clic aquí para WhatsApp* → https://wa.me/573114844532?text=Hola,%20adjunto%20mi%20comprobante%20de%20pago
            (Solo abre el enlace y envía el archivo)

            Gracias por elegirnos 🌟
            Cualquier duda, estamos para ti.

            Saludos,
            El equipo de San Felipe
            """

            send_mail(
                subject="🎉 Pedido confirmado - San Felipe",
                message=mensaje_usuario,
                from_email="soportesanfelipe324@gmail.com",
                recipient_list=[usuario.email],
                fail_silently=False,
            )

            # 📩 Correo para la Empresa
            mensaje_empresa = f"""
            🔔 Nuevo pedido en San Felipe

            Cliente: {usuario.first_name} {usuario.last_name}
            Email: {usuario.email}
            ___________________________
            {pedido_texto}
            ___________________________

            💰 Total: ${total}
            💳 Método de pago: {metodo_pago}

            📌 Acción: Verificar y preparar el pedido ASAP.

            Saludos,
            Sistema San Felipe
            """

            send_mail(
                subject="🔔 Nuevo pedido - San Felipe",
                message=mensaje_empresa,
                from_email="soportesanfelipe324@gmail.com",
                recipient_list=["andresbustos170@gmail.com"],
                fail_silently=False,
            )

            return JsonResponse({"mensaje": "Pedido enviado, guardado y correos enviados correctamente."})

        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Error en los datos enviados"}, status=400)
        except Exception as e:
            return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"mensaje": "Método no permitido"}, status=405)


def index_view(request):
    """Vista principal que muestra la página inicial."""
    return render(request, 'index.html')

@login_required
def pedido_view(request):
    """Vista para mostrar y confirmar pedidos (solo usuarios autenticados)."""
    return render(request, 'pedido.html')

def index(request):
    return render(request, 'index.html', {'user_authenticated': request.user.is_authenticated})

def pedido(request):
    return render(request, "pedido.html")

def reservar(request):
    return render(request, "reservar.html")

def tienda(request):
    productos = Producto.objects.filter(disponible=True)  # Filtrar solo disponibles
    return render(request, "tienda.html", {'productos': productos, 'user_authenticated': request.user.is_authenticated})

@login_required
def perfil(request):
    try:
        perfil = request.user.perfil  # Access the user's profile
    except PerfilUsuario.DoesNotExist:
        perfil = None
    pedidos = Pedido.objects.filter(usuario=request.user)  # Fetch all orders for the user
    context = {
        'perfil': perfil,
        'pedidos': pedidos,
    }
    return render(request, 'perfil_usuario.html', context)

def confirmar_pedido(request):
    if request.method == "POST":
        return JsonResponse({"mensaje": "Pedido confirmado correctamente"}, status=200)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def nosotros_view(request):
    return render(request, "nosotros.html")

def recuperar(request):
    return render(request, "recuperar.html")

def manual(request):
    return render(request, "manual.html")

def sugerencias(request):
    return render(request, "sugerencias.html")

def sugerencia_view(request):
    return JsonResponse({'message': 'Vista de sugerencias funcionando correctamente'})

def logout_view(request):
    logout(request)
    return redirect('/')

def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related('items')
    return render(request, 'historial.html', {'pedidos': pedidos})

@csrf_protect
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")

            if new_password1 and new_password2 and new_password1 == new_password2:
                if len(new_password1) < 8:
                    return JsonResponse({"success": False, "error": "La contraseña debe tener al menos 8 caracteres."})
                user.set_password(new_password1)
                user.save()
                return JsonResponse({"success": True, "redirect_url": "/login/"})
            else:
                return JsonResponse({"success": False, "error": "Las contraseñas no coinciden o están vacías."})
        
        # Renderiza la plantilla con uidb64 y token en el contexto
        return render(request, 'password_reset_confirm.html', {
            'uidb64': uidb64,
            'token': token
        })
    else:
        messages.error(request, "El enlace de restablecimiento es inválido o ha expirado.")
        return redirect('/login/')

@login_required(login_url='/login/')
def procesar_pedido(request):
    if request.method == 'POST':
        try:
            # Obtener el carrito desde el POST
            carrito = json.loads(request.POST.get('carrito', '[]'))
            if not carrito:
                return redirect('tienda')  # Redirige si el carrito está vacío

            # Crear el pedido
            pedido = Pedido.objects.create(usuario=request.user)
            
            # Agregar ítems al pedido
            for item in carrito:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto_id=item['id'],  # Asume que el carrito tiene el ID del producto
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio']
                )
            
            return redirect('historial')
        except Exception as e:
            print(f"Error al procesar el pedido: {e}")
            return redirect('tienda')  # Redirige en caso de error
    
    return redirect('tienda')




















