# Generated by Django 2.0.5 on 2018-06-01 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20180601_0507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stylesettings',
            name='site',
        ),
        migrations.DeleteModel(
            name='StyleSettings',
        ),
    ]
