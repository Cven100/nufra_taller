# Generated by Django 5.1 on 2024-11-22 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='jefatura',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
