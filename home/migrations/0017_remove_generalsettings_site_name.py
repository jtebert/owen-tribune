# Generated by Django 2.0.5 on 2018-06-14 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20180610_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalsettings',
            name='site_name',
        ),
    ]
