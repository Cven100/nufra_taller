# Generated by Django 5.1 on 2024-11-25 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_pedido_estado_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateField(),
        ),
    ]
