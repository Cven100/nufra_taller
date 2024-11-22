import datetime
from django.contrib import messages

#SESSION
from django.contrib.auth import logout

#HTTP
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from app.forms import CategoriaProducto, CategoriaProductoForm, InventarioForm, LoginForm, ProductoForm, ProveedorForm, RegisterForm, VentaForm

#MODEL
from .models import DetalleVenta, Empleado, Producto, Venta



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
    return redirect('login')

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
    """Funcion que renderiza el home de la pagina"""
    return render(request, 'shared/home.html')


#ADMNISTRADOR
def RenderAdminHome(request):
    return render(request, 'admin/adminHome.html')

def RenderGestionTienda(request):
    return render(request, 'admin/gestionTienda/gestionTienda.html')
def RenderCrearProductos(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crearProductos")
    else:
        form = ProductoForm()
    return render(request, "admin/gestionTienda/crearProductos.html", {"form": form})    


def RenderGestionProductos(request):
    return render(request, 'admin/gestionTienda/gestionProductos.html')
def RenderCategorias(request):
    categorias = CategoriaProducto.objects.all()
    form = CategoriaProductoForm()
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categorias")
    data = {"form": form, "categorias": categorias}
    return render(request, 'admin/gestionTienda/categorias.html', data)

def RenderProveedores(request):
    return render(request, 'admin/proveedores/proveedores.html')
def RenderGestionProveedores(request):
    return render(request, 'admin/proveedores/gestionProveedores.html')
def RenderCrearProveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crearProveedor")
    else:
        form = ProveedorForm()
    return render(request, 'admin/proveedores/crearProveedor.html', {"form": form})
def RenderPedidos(request):
    return render(request, 'admin/proveedores/pedidos.html')

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
    carrito = request.session.get("carrito", [])
    empleado = request.session["nombre", "nombre del vendedor"]

    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            cantidad = form.cleaned_data["cantidad"]

            try:
                producto = Producto.objects.get(codigo= codigo)
            except Producto.DoesNotExist:
                messages.error(request, "El producto no existe.")
                return redirect("venta")
            subtotal = producto.precio_venta * cantidad

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

            request.session["carrito"] = carrito

            return redirect("venta")
        
    elif request.method == "GET":
        form = VentaForm()
        return render(request, "vendedor/venta.html", {"form": form, "carrito": carrito, "empleado": empleado} )
   


    
    