# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad', models.CharField(choices=[('U', 'Unidad'), ('M', 'metro'), ('L', 'litro')], max_length=1)),
                ('cantida', models.IntegerField()),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('S', 'solicsitud'), ('A', 'aprovado'), ('R', 'rechazado')], max_length=1)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizacion.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizacion.Producto'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizacion.Proveedor'),
        ),
    ]