# Generated by Django 5.1.2 on 2024-11-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0005_rename_precio_producto_porc_ganancias_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='cantidad_art',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
