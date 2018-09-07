# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0003_auto_20171127_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='mesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesa', models.IntegerField(unique=True)),
                ('nulos', models.IntegerField()),
                ('blancos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='votos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField()),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votaciones.mesa')),
                ('partidos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votaciones.partidos')),
            ],
        ),
    ]