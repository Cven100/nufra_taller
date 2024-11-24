import datetime
from django.contrib import messages

#SESSION
from django.contrib.auth import logout

#HTTP
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from app.forms import CategoriaProducto, CategoriaProductoForm, InventarioForm, LoginForm, ProductoForm, ProveedorForm, RealizarPedido, RegisterForm, VentaForm

#MODEL
from .models import DetallePedido, DetalleVenta, Empleado, Pedido, Producto, Proveedor, Venta

from django.db.models import Q




def vendedor_required(view_func):
    """Función decoradora que asegura que el usuario tenga rol de Vendedor."""
    def wrapper(request, *args, **kwargs):
        """Wrapper protector que valida el rol de vendedor antes de permitir el acceso."""
        if request.session.get('user_id') and request.session.get('rol_id') in ["1", "2", "3"]:  # '2' para rol de vendedor
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return wrapper

def supervisor_required(view_func):
    """Función decoradora que asegura que el usuario tenga rol de Supervisor."""
    def wrapper(request, *args, **kwargs):
        """Wrapper protector que valida el rol de Supervisor antes de permitir el acceso."""
        if request.session.get('user_id') and request.session.get('rol_id') in ["1", "2"]:  # '3' para rol de supervisor
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return wrapper

def admin_required(view_func):
    """Función decoradora que asegura que el usuario tenga rol de administrador."""
    def wrapper(request, *args, **kwargs):
        """Wrapper protector que valida el rol de administrador antes de permitir el acceso."""
        # rol_id se basan en los de bd
        if request.session.get('user_id') and request.session.get('rol_id') == '1':
            return view_func(request, *args, **kwargs)
        return redirect('Login')  # Redirige al login si no es admin
    return wrapper


def Logout(request):
    logout(request)  # Limpia la sesión del usuario
    return redirect('home')

def RenderLogin(request):
    if request.method == 'POST':
        login = LoginForm(request.POST)
        if login.is_valid():
            # cleaned_data es el diccionario que contiene los campos del modelo
            username = login.cleaned_data['username']
            password = login.cleaned_data['password']

            try:
                empleado = Empleado.objects.get(username=username)
                if empleado.check_password(password):
                    request.session['nombre'] = empleado.nombre
                    request.session['rut_empleado'] = empleado.rut_empleado
                    request.session['rol_id'] = str(empleado.rol.id) 
                    if empleado.rol.id == 1:
                        return redirect('adminHome')  # Rol de admin
                    elif empleado.rol.id == 2:
                        return redirect('superHome')  # Rol de superusuario
                    elif empleado.rol.id == 3:
                        return redirect('venta')  # Rol de usuario estándar
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Credenciales Incorrectas')
                    return render(request, 'shared/login.html', {'form': login})
            except Empleado.DoesNotExist:
                messages.error(request, 'Empleado no existe')
                return render(request, 'shared/login.html', {'form': login})
        else:
            messages.error(request, 'Formulario invalido')
            return render(request, 'shared/login.html', {'form': login})

    elif request.method == 'GET':
        formLogin = LoginForm()
        return render(request, 'shared/login.html', {'form': formLogin})

def RenderRegister(request):
    
    has_error = {}
    if request.method == 'POST':
        register = RegisterForm(request.POST)
        if register.is_valid():
            empleado = register.save(commit=False)  # asigna la variable, pero aun no guarda en db
            empleado.set_password(empleado.password)  # encripta
            empleado.save()                         # guarda
            return redirect('home')
        else:
            has_error['register_error'] = 'Un campo fue ingresado incorrectamente'
            return render(request, 'admin/personal/register.html', {'form': register, 'error': has_error}) 
    
    elif request.method == 'GET':
        form = RegisterForm()
        return render(request, 'admin/personal/register.html', {'form': form})
    
#SHARED
def RenderHome(request):
    """Función que renderiza el home de la página."""
    data = {
        'rut_empleado': request.session.get('rut_empleado'),
        'rol_id': request.session.get('rol_id'),
    }
    return render(request, 'shared/home.html', data)


#ADMNISTRADOR
def RenderAdminHome(request):
    return render(request, 'admin/adminHome.html')


def RenderGestionProductos(request, producto_codigo=None):
    query = request.GET.get('search', '')  # Obtener el término de búsqueda del input
    productos = Producto.objects.filter(
        Q(nombre__icontains=query)  # Buscar por nombre de producto (insensible a mayúsculas/minúsculas)
    ) if query else Producto.objects.all()  # Si no hay búsqueda, mostrar todos los productos
    producto = None
    if producto_codigo:
        producto = get_object_or_404(Producto, codigo=producto_codigo)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("productos")
    else:
        form = ProductoForm(instance=producto)
    context = {
        'productos': productos,
        'producto': producto,
        'query': query,
        "form": form  # Mantener el término buscado en el input
    }
    return render(request, 'admin/gestionTienda/gestionProductos.html', context)



def DeshabilitarProducto(request, producto_codigo):
    producto = get_object_or_404(Producto, codigo=producto_codigo)
    producto.disponible = not producto.disponible
    producto.save()
    return redirect('categorias')  # Redirigir a la lista de productos



def RenderGestionCategorias(request, categoria_id=None):
    query = request.GET.get('search', '') 
    categorias = CategoriaProducto.objects.filter(
        Q(nombre__icontains=query) 
    ) if query else CategoriaProducto.objects.all()
    categoria = None
    if categoria_id:
        categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categorias")
    else:
        form = CategoriaProductoForm(instance=categoria)
    data = {"form": form, "categorias": categorias, "query":query, "categoria":categoria}
    return render(request, 'admin/gestionTienda/gestionCategorias.html', data)

def DeshabilitarCategoria(request, categoria_id):
    categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
    categoria.disponible = not categoria.disponible
    categoria.save()
    return redirect("categorias")


def RenderGestionProveedores(request, proveedor_id=None):
    proveedor = None
    if proveedor_id:
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect("proveedores")  # Redirigir a la lista tras guardar
    else:
        form = ProveedorForm(instance=proveedor)

    proveedores = Proveedor.objects.all().order_by("nombre")

    return render(request, "admin/proveedores/gestionProveedores.html", {
        "form": form,
        "proveedores": proveedores,
        "proveedor": proveedor 
    })



def DeshabilitarProveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.disponible = not proveedor.disponible
    proveedor.save()
    return redirect('proveedores') 


def RenderCrearPedido(request, proveedor_id):
    query = request.GET.get('search', '')
    productos = Producto.objects.filter(proveedor_id=proveedor_id)
    if query:
        productos = productos.filter(Q(nombre__icontains=query))  # Buscar por nombre de producto
    
    pedido = request.session.get('pedido', [])
    if request.method == "POST":
        codigo_producto = request.POST.get('codigo')
        cantidad = int(request.POST.get('cantidad'))

        try:
            producto = Producto.objects.get(codigo=codigo_producto)

            # Verificar si el producto ya está en el carrito
            producto_en_carrito = next((item for item in pedido if str(item['codigo']) == str(codigo_producto)), None)

            if producto_en_carrito:
                # Si el producto ya está en el carrito, sumar la cantidad
                producto_en_carrito['cantidad'] += cantidad
                producto_en_carrito['subtotal'] = producto_en_carrito['cantidad'] * producto.precio_compra
            else:
                # Si el producto no está en el carrito, añadirlo
                pedido.append({
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'precio_unitario': producto.precio_compra,
                    'cantidad': cantidad,
                    'subtotal': cantidad * producto.precio_compra
                })

            # Guardar el carrito en la sesión
            request.session['pedido'] = pedido
            messages.success(request, 'Producto agregado al carrito.')

        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado.')

        return redirect('crearPedido', proveedor_id=proveedor_id)  # Redirigir a la misma página para ver el carrito actualizado
    
    return render(request, "admin/proveedores/crearPedido.html", {
        'productos': productos,
        'query': query,
        'proveedor_id': proveedor_id,
        'pedido': pedido,  # Pasar el carrito a la plantilla
    })


def EliminarProductoPedido(request, codigo_producto, proveedor_id):
    if request.method == "POST":
        if "pedido" in request.session:
            request.session["pedido"] = [
                item for item in request.session["pedido"] if item["codigo"] != codigo_producto
            ]
            request.session.modified = True 
            messages.success(request, "Producto eliminado del pedido.")
        else:
            messages.error(request, "No se pudo encontrar el pedido en la sesión.")
        return redirect('crearPedido', proveedor_id=proveedor_id)





def ConfirmarPedido(request):
    total_pedido = 0
    proveedor = None 

    for item in request.session["pedido"]:
        producto = Producto.objects.get(codigo=item["codigo"])
        if proveedor is None:
            proveedor = producto.proveedor

    if proveedor is None:
        messages.error(request, "No se ha encontrado un proveedor para el pedido.")
        return redirect("pedidos")

    pedido = Pedido.objects.create(
        proveedor=proveedor,
        total_pedido=total_pedido,
    )

    for item in request.session["pedido"]:
        producto = Producto.objects.get(codigo=item["codigo"])
        cantidad = item["cantidad"]
        subtotal = item["subtotal"]
        
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio_compra,
            subtotal=subtotal,
        )

        producto.stock -= cantidad
        producto.save()
        total_pedido += subtotal
    pedido.total_pedido = total_pedido
    pedido.save()
    request.session["pedido"] = []
    request.session.modified = True
    messages.success(request, f"Pedido {pedido.nro_pedido} confirmado y stock actualizado.")
    return redirect("proveedores")




def RenderPersonal(request):
    return render(request, 'admin/personal/personal.html')

def RenderReportes(request):
    return render(request, 'admin/reportes/reportes.html')


#sUPERVISOR
def RenderSuperHome(request):
    return render(request, 'supervisor/superHome.html')

def RenderInventario(request):
    return render(request, "supervisor/inventario.html")


def RenderIngresoMermas(request):
    return render(request, 'supervisor/ingresoMermas.html')

def RenderRecepcionPedido(request):
    return render(request, 'supervisor/recepcionPedido.html')


#VENDEDOR
def RenderVenta(request):
    carrito = request.session.get("carrito_venta", [])
    empleado = request.session.get("nombre", "Empleado no identificado")
    rol_id = request.session.get("rol_id", "0")  # Aquí obtienes el rol de la sesión como string


    total_compra = sum(item['subtotal'] for item in carrito)

    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            cantidad = form.cleaned_data["cantidad"]

            # Validación básica de cantidad
            if cantidad <= 0:
                messages.error(request, "La cantidad debe ser mayor que cero.")
                return render(request, "vendedor/venta.html", {"form": form, "carrito": carrito, "empleado": empleado, "total_compra": total_compra})

            try:
                producto = Producto.objects.get(codigo=codigo)
            except Producto.DoesNotExist:
                messages.error(request, "El producto no existe.")
                return render(request, "vendedor/venta.html", {"form": form, "carrito": carrito, "empleado": empleado, "total_compra": total_compra})

            # Validación de stock
            if producto.stock < cantidad:
                messages.error(request, f"Stock insuficiente. Solo quedan {producto.stock} unidades de {producto.nombre}.")
                return render(request, "vendedor/venta.html", {"form": form, "carrito": carrito, "empleado": empleado, "total_compra": total_compra})

            subtotal = producto.precio_venta * cantidad

            # Actualizar o agregar al carrito
            for item in carrito:
                if item["codigo"] == producto.codigo:
                    item["cantidad"] += cantidad
                    item["subtotal"] = item["cantidad"] * item["precio_unitario"]
                    break
            else:
                carrito.append({
                    "codigo": producto.codigo,
                    "nombre": producto.nombre,
                    "precio_unitario": producto.precio_venta,
                    "cantidad": cantidad,
                    "subtotal": subtotal,
                })

            # Actualizar el carrito en la sesión
            request.session["carrito_venta"] = carrito
            return redirect("venta")

    else:
        form = VentaForm()

    return render(request, "vendedor/venta.html", {
        "form": form, 
        "carrito": carrito, 
        "empleado": empleado,
        "rol_id": rol_id,
        "total_compra": total_compra  # Pasamos el total de la compra al template
    })

def ConfirmarVenta(request):
    carrito = request.session.get("carrito_venta", [])
    empleado_rut = request.session.get("rut_empleado", "")  # Obtener el RUT del empleado desde la sesión

    # Validar que el carrito no esté vacío
    if not carrito:
        messages.error(request, "El carrito está vacío. No se puede confirmar la compra.")
        print("Carrito vacío, redirigiendo...")
        return redirect("venta")

    try:
        # Obtener la instancia de Empleado utilizando el rut_empleado desde la sesión
        empleado = Empleado.objects.get(rut_empleado=empleado_rut)
        print(f"Empleado encontrado: {empleado}")

        # Crear la instancia de Venta
        venta = Venta.objects.create(
            empleado=empleado,  # Asignamos la instancia de Empleado
            total_venta=0,  # Se calculará posteriormente
        )

        total_venta = 0

        # Crear las instancias de DetalleVenta y actualizar el stock
        for item in carrito:
            producto = Producto.objects.get(codigo=item["codigo"])

            if producto.stock < item["cantidad"]:
                messages.error(request, f"Stock insuficiente para {producto.nombre}. No se puede completar la compra.")
                venta.delete()  # Deshacer la venta si hay un error
                return redirect("venta")

            # Crear el detalle de la venta
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
                subtotal=item["subtotal"],
            )

            # Actualizar el stock del producto
            producto.stock -= item["cantidad"]
            producto.save()

            # Sumar el subtotal al total de la venta
            total_venta += item["subtotal"]

        # Actualizar el total de la venta
        venta.total_venta = total_venta
        venta.save()

        # Limpiar el carrito
        request.session["carrito_venta"] = []

        # Mensaje de éxito
        messages.success(request, f"Compra confirmada. Venta registrada con ID {venta.nro_boleta}.")
        return redirect("venta")

    except Empleado.DoesNotExist:
        messages.error(request, f"No se encontró el empleado con RUT {empleado_rut}.")
        return redirect("venta")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al confirmar la compra: {str(e)}")
        return redirect("venta")

def QuitarProductoCarrito(request, codigo):
    carrito_venta = request.session.get("carrito_venta", [])
    # Filtrar los productos del carrito eliminando el producto con el código especificado
    carrito_venta = [p for p in carrito_venta if p["codigo"] != codigo]
    request.session["carrito_venta"] = carrito_venta
    return redirect("venta")

