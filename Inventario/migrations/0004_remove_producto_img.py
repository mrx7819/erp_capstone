# Generated by Django 5.1.2 on 2024-12-07 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_producto_iva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='img',
        ),
    ]
