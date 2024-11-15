# Generated by Django 5.1.2 on 2024-11-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0002_remove_producto_cantidad_producto_capacidad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bodega',
            old_name='cantidad',
            new_name='cantidad_art',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='capacidad',
            new_name='cantidad',
        ),
        migrations.AddField(
            model_name='bodega',
            name='capacidad',
            field=models.IntegerField(default=0),
        ),
    ]
