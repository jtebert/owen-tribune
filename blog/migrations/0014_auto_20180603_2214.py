# Generated by Django 2.0.5 on 2018-06-03 22:14

import blog.models
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20180602_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('captioned_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(blank=True, help_text='This will override the default caption.This text will be formatted with markdown.', null=True, required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('pull_quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock()), ('author', wagtail.core.blocks.CharBlock())])), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blog/table_block.html')), ('media', wagtail.core.blocks.StructBlock([('media', blog.models.MediaBlock()), ('show_controls', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('autoplay', wagtail.core.blocks.BooleanBlock(required=False)), ('loop', wagtail.core.blocks.BooleanBlock(required=False)), ('muted', wagtail.core.blocks.BooleanBlock(required=False))]))]),
        ),
    ]
