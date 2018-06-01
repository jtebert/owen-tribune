# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 19:21
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161213_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='subject_1',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='subject_2',
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.core.fields.StreamField([(b'text', wagtail.core.blocks.TextBlock(help_text=b'This text will be formatted with markdown.', icon=b'pilcrow')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.CharBlock(blank=True, help_text=b'This will override the default caption.This text will be formatted with markdown.', null=True, required=False))])), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon=b'media')), (b'pull_quote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock()), (b'author', wagtail.core.blocks.CharBlock())]))]),
        ),
    ]
