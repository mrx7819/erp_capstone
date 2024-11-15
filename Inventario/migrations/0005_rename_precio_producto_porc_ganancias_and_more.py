# Generated by Django 5.1.2 on 2024-11-15 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0004_remove_bodega_producto_producto_bodega'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='precio',
            new_name='porc_ganancias',
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_compra',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_venta',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bodega',
            name='direccion',
            field=models.CharField(max_length=100),
        ),
    ]
