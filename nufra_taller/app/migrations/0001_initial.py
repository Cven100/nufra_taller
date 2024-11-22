# Generated by Django 5.1 on 2024-11-22 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('nro_pedido', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('precio_total', models.FloatField(default=0)),
                ('total_pedido', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=100)),
                ('correo', models.EmailField(max_length=255)),
                ('telefono', models.CharField(max_length=16)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categoriaproducto')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('precio_venta', models.FloatField()),
                ('precio_compra', models.FloatField()),
                ('disponible', models.BooleanField(default=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/')),
                ('stock', models.IntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.categoriaproducto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detallePedido', to='app.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='app.inventario')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.proveedor'),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('rut_empleado', models.CharField(max_length=14, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(default='', max_length=150)),
                ('apellido', models.CharField(default='', max_length=150)),
                ('correo', models.EmailField(default='', max_length=255, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('telefono', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=128)),
                ('jefatura', models.CharField(max_length=16)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.roles')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('nro_boleta', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total_venta', models.FloatField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalleVenta', to='app.venta')),
            ],
        ),
    ]
