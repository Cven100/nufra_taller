from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from app import views as vistas
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Control de acceso
    path('', vistas.RenderHome, name='home'),
    path('login/', vistas.RenderLogin, name='login'),
    path('register/', vistas.RenderRegister, name='register'),
    path('logout/', vistas.Logout, name='logout'),
    
    # Admin
    path('adminHome', vistas.RenderAdminHome, name='adminHome'),

    path('gestionTienda', vistas.RenderGestionTienda, name='gestionTienda'),
    path('crearProductos', vistas.RenderCrearProductos, name='crearProductos'),
    path('gestionProductos', vistas.RenderGestionProductos, name='gestionProductos'),
    path('categorias', vistas.RenderCategorias, name='categorias'),

    path('proveedores', vistas.RenderProveedores, name='proveedores'),
    path('gestionProveedores', vistas.RenderGestionProveedores, name='gestionProveedores'),
    path('crearProveedor', vistas.RenderCrearProveedor, name='crearProveedor'),
    path('pedidos', vistas.RenderPedidos, name='pedidos'),

    path('personal', vistas.RenderPersonal, name='personal'),
    
    path('reportes', vistas.RenderReportes, name='reportes'),

    #     #Proveedor
    # path('home/admin/config/proveedores/', vistas.RenderProveedores, name='proveedores'),
    # path('home/admin/config/add-proveedor/', vistas.AddProveedor, name='addProveedor'),
    # path('home/admin/config/edit-proveedor/<int:id>/', vistas.EditProveedor, name='editProveedor'),
    # #Block/Unblock Proveedor
    # path('home/admin/config/block-proveedor/<int:id>/', vistas.BlockProveedor, name='blockProveedor'),
    
    #     #Producto
    # path('home/admin/config/productos/', vistas.RenderProducto, name='productos'),
    # path('home/admin/config/add-producto/', vistas.AddProducto, name='addProducto'),
    # path('home/admin/config/edit-producto/<int:id>/', vistas.EditProducto, name='editProducto'),
    # #Block/Unblock Producto
    # path('home/admin/config/productos/block-producto/<int:id>/', vistas.BlockProducto, name='blockProducto'),

    #     #Categorias
    # path('home/admin/config/productos/categorias/', vistas.RenderCategorias, name='categorias'),
    # path('home/admin/config/productos/categorias/edit-categoria/<int:id>/', vistas.EditCategoria, name='editCategoria'),
    
    # #Block/Unblock categoria
    # path('home/admin/config/productos/categorias/block-categoria/<int:id>/', vistas.BlockCategoria, name='blockCategoria'),

    # # Supervisor
    path('superHome', vistas.RenderSuperHome, name='superHome'),
    path('inventario', vistas.RenderInventario, name='inventario'),
    path('ingresoMermas', vistas.RenderIngresoMermas, name='ingresoMermas'),
    path('recepcionPedido', vistas.RenderRecepcionPedido, name='recepcionPedido'),

    
    # # Vendedor
    path('venta/', vistas.RenderVenta, name='venta'),


   #  DOCUMENTACION
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)