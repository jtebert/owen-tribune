# Generated by Django 2.0.5 on 2018-06-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20180604_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='intro',
            field=models.TextField(help_text='This will only appear in article previews, not with the full article.This text will be formatted with markdown.', max_length=480),
        ),
    ]
