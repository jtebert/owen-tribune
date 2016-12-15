# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20161213_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorpage',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='authorpage',
            name='personal_website',
        ),
        migrations.AddField(
            model_name='authorpage',
            name='long_bio',
            field=models.TextField(blank=True, help_text=b'This text will appear on the author page.This text will be formatted with markdown.', null=True),
        ),
        migrations.AddField(
            model_name='authorpage',
            name='short_bio',
            field=models.TextField(blank=True, help_text=b'This text will appear at the end of articles.This text will be formatted with markdown.', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='authorpage',
            name='twitter_handle',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
