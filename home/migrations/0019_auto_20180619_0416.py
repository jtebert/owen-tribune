# Generated by Django 2.0.5 on 2018-06-19 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_generalsettings_google_custom_search_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previewarticle',
            name='article',
        ),
        migrations.RemoveField(
            model_name='previewarticle',
            name='page',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.DeleteModel(
            name='PreviewArticle',
        ),
    ]
