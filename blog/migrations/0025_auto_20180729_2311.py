# Generated by Django 2.0.5 on 2018-07-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20180722_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiencepage',
            options={'verbose_name': 'Audience'},
        ),
        migrations.AlterField(
            model_name='audiencepage',
            name='intro',
            field=models.TextField(blank=True, max_length=480, null=True),
        ),
    ]