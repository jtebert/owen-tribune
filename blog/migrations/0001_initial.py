# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 17:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.')),
            ],
            options={
                'verbose_name': 'Article Index',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleIndexRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name=b'External link')),
                ('title', models.CharField(help_text=b'Link title', max_length=255)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name=b'Post date')),
                ('intro', models.TextField(help_text=b'This will only appear in article previews, not with the full article.This text will be formatted with markdown.', max_length=250)),
                ('body', wagtail.core.fields.StreamField([(b'text', wagtail.core.blocks.TextBlock(help_text=b'This text will be formatted with markdown.', icon=b'pilcrow')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.CharBlock(blank=True, help_text=b'This will override the default caption.This text will be formatted with markdown.', null=True, required=False))])), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon=b'media')), (b'extra_information', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock()), (b'text', wagtail.core.blocks.TextBlock(help_text=b'This text will be formatted with markdown.'))]))])),
            ],
            options={
                'verbose_name': 'Article',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleSourceLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.Use a standard citation format.', max_length=1023, null=True)),
                ('url', models.URLField(blank=True, null=True, verbose_name=b'Link to Source')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_links', to='blog.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuthorIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AuthorPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('bio', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.', max_length=800, null=True)),
                ('personal_website', models.URLField(blank=True)),
                ('portrait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AuthorSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=255)),
                ('bio', models.TextField(max_length=800, null=True)),
                ('homepage', models.URLField(blank=True)),
                ('portrait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Author',
            },
        ),
        migrations.CreateModel(
            name='SubjectCategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Subject Category',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubjectIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubjectPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.TextField(blank=True, help_text=b'This text will be formatted with markdown.', max_length=800, null=True)),
            ],
            options={
                'verbose_name': 'Subject',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.AuthorPage'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='main_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='subject_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.SubjectPage'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='subject_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.SubjectPage'),
        ),
        migrations.AddField(
            model_name='articleindexrelatedlink',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='articleindexrelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='blog.ArticleIndexPage'),
        ),
    ]
