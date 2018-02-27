# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-26 20:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('blog', '0009_auto_20180226_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'text', wagtail.wagtailcore.blocks.TextBlock(help_text=b'This text will be formatted with markdown.', icon=b'pilcrow')), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(blank=True, help_text=b'This will override the default caption.This text will be formatted with markdown.', null=True, required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'pull_quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.TextBlock()), (b'author', wagtail.wagtailcore.blocks.CharBlock())])), (b'table', wagtail.contrib.table_block.blocks.TableBlock(template=b'blog/table_block.html'))]),
        ),
        migrations.AddField(
            model_name='articlepagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.ArticlePage'),
        ),
        migrations.AddField(
            model_name='articlepagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_articlepagetag_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.ArticlePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]