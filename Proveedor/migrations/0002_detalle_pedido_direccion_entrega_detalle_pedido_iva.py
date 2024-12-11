# Generated by Django 5.1.2 on 2024-12-06 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0002_initial'),
        ('Proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_pedido',
            name='direccion_entrega',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='Inventario.bodega'),
        ),
        migrations.AddField(
            model_name='detalle_pedido',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=19.0, max_digits=5),
        ),
    ]
