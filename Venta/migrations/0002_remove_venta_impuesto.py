# Generated by Django 5.1.2 on 2024-12-04 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Venta', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='impuesto',
        ),
    ]