# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='level4appcategory',
            name='cat_rank',
            field=models.IntegerField(default=0, verbose_name='rank'),
        ),
        migrations.AlterField(
            model_name='level1bizgroup',
            name='bg_id',
            field=models.IntegerField(default=1, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='level2workgroup',
            name='wg_id',
            field=models.IntegerField(default=1, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='level3app',
            name='app_id',
            field=models.IntegerField(default=1, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='level5applink',
            name='link_name',
            field=models.CharField(default='DEFAULT', max_length=50, unique=True, verbose_name='name'),
        ),
    ]