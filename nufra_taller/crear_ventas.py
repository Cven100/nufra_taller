# documento para crear ventas aleadtorias en los ultimos 3 meses, es importante quitar el autoadd de datetime en modelo de venta para que funcione correctamente

# import random
# from datetime import datetime, timedelta
# import os
# import django

# # Establecer la variable de entorno para Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nufra_taller.settings')

# # Configurar Django
# django.setup()

# # Ahora importa los modelos
# from app.models import Venta, DetalleVenta, Empleado, Producto
# from app.models import Producto

# # Actualizar el stock de todos los productos a 1000
# productos = Producto.objects.all()

# # Recorrer todos los productos y actualizar su stock
# for producto in productos:
#     producto.stock = 1000  # Asigna 1000 unidades a cada producto
#     producto.save()  # Guarda los cambios en la base de datos

# print("Stock actualizado a 1000 para todos los productos.")



# # Configurar la fecha base (25/11/2024)
# fecha_base = datetime(2024, 11, 25)

# # Obtener empleados y productos existentes
# empleados = list(Empleado.objects.all())
# productos = list(Producto.objects.filter(disponible=True, stock__gt=0))

# # Función para generar una fecha aleatoria en los últimos 3 meses
# def fecha_aleatoria(base, meses_atras):
#     dias_atras = meses_atras * 30
#     fecha_random = base - timedelta(days=random.randint(0, dias_atras))
#     return fecha_random.date()

# # Crear 100 ventas
# for _ in range(100):
#     # Seleccionar un empleado al azar
#     empleado = random.choice(empleados)

#     # Generar una fecha aleatoria en los últimos 3 meses
#     fecha = fecha_aleatoria(fecha_base, 3)

#     # Crear la venta
#     venta = Venta(
#         empleado=empleado,
#         fecha=fecha,
#         total_venta=0,  # Se calculará después
#     )
#     venta.save()

#     # Generar entre 1 y 5 productos para esta venta
#     total_venta = 0
#     for _ in range(random.randint(1, 5)):
#         producto = random.choice(productos)
#         cantidad = random.randint(1, min(10, producto.stock))  # Máximo 10 unidades o lo que haya en stock
#         precio_unitario = int(producto.precio_venta)
#         subtotal = cantidad * precio_unitario

#         # Crear el detalle de la venta
#         detalle = DetalleVenta(
#             venta=venta,
#             producto=producto,
#             cantidad=cantidad,
#             precio_unitario=precio_unitario,
#             subtotal=subtotal,
#         )
#         detalle.save()

#         # Reducir el stock del producto
#         producto.stock -= cantidad
#         producto.save()

#         # Acumular el total de la venta
#         total_venta += subtotal

#     # Actualizar el total de la venta
#     venta.total_venta = total_venta
#     venta.save()

# print("100 ventas creadas exitosamente.")
