# Generated by Django 5.1.2 on 2024-12-04 00:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0002_remove_venta_impuesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_venta',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
