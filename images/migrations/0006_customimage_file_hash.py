# Generated by Django 2.1.4 on 2018-12-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20180601_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='file_hash',
            field=models.CharField(blank=True, editable=False, max_length=40),
        ),
    ]