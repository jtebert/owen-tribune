# Generated by Django 2.0.5 on 2018-07-22 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20180619_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopage',
            name='notes',
            field=models.TextField(blank=True, help_text='This text will not appear on the page.', null=True),
        ),
    ]