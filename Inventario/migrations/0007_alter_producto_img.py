# Generated by Django 5.1.2 on 2024-12-11 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0006_remove_producto_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='img',
            field=models.ImageField(blank=True, upload_to='productos/'),
        ),
    ]
