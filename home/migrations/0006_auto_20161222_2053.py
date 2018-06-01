# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 20:53
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20161213_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalsettings',
            name='favicon',
        ),
        migrations.AlterField(
            model_name='infopage',
            name='body',
            field=wagtail.core.fields.StreamField((('text', wagtail.core.blocks.TextBlock(help_text='This text will be formatted with markdown.', icon='pilcrow')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(blank=True, help_text='This will override the default caption.This text will be formatted with markdown.', null=True, required=False))))), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')))),
        ),
    ]
