# Generated by Django 2.0.8 on 2019-01-21 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0013_auto_20190120_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='categoria',
            field=models.CharField(choices=[('extra', 'Extra'), ('practica', 'Práctica'), ('ejclase', 'Ejercicios clase'), ('proyecto', 'Proyecto'), ('tarea', 'Tarea'), ('examen', 'Examen')], max_length=50),
        ),
    ]