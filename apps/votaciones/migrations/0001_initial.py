# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='nuevaEleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_eleccion', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='partidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_partido', models.CharField(max_length=60)),
                ('nuevaEleccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votaciones.nuevaEleccion')),
            ],
        ),
    ]
