# Generated by Django 5.1.2 on 2024-12-07 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0005_remove_categoria_img_producto_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='descripcion',
        ),
    ]