from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks, hooks
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail.contrib.settings.models import BaseSetting, register_setting

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

import blog.models

md_format_help = 'This text will be formatted with markdown.'
DEFAULT_RICHTEXT_FEATURES = [
    'h2', 'h3', 'h4', 'h5',
    'bold', 'italic', 'strikethrough', 'code',
    'ol', 'ul',
    'hr',
    'link',
    'document-link',
]


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']

    featured_article = models.ForeignKey(
        blog.models.ArticlePage,
        null=True, blank=True,
        on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        PageChooserPanel('featured_article'),
    ]

    class Meta:
        verbose_name = "Homepage"

    def latest_articles(self):
        articles = blog.models.ArticlePage.objects.live()
        if self.featured_article:
            articles.exclude(pk=self.featured_article.pk)
        articles = articles.order_by('-date')
        return articles[0:5]


class InfoPage(Page):
    subpage_types = []

    body = StreamField([
        ('text', blocks.RichTextBlock(features=DEFAULT_RICHTEXT_FEATURES)),
        ('captioned_image', blog.models.CaptionedImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('block_quote', blog.models.QuoteBlock()),
        ('table', blog.models.TableBlock(template='blog/table_block.html')),
        ('media', blog.models.OptionsMediaBlock()),
        ('code', blog.models.CodeBlock()),
    ])
    notes = models.TextField(
        null=True, blank=True,
        help_text="This text will not appear on the page.")

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('notes'),
    ]

    class Meta:
        verbose_name = 'Information Page'


@hooks.register('register_rich_text_features')
def register_code_feature(features):
    """
    Registering the `code` feature, which uses the `CODE` Draft.js inline style type,
    and is stored as HTML with an `<s>` tag.
    """
    feature_name = 'code'
    type_ = 'CODE'
    tag = 'code'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': '</>',
        'description': 'Code',
        # This isn’t even required – Draftail has predefined styles for STRIKETHROUGH.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule(
        'contentstate', feature_name, db_conversion)


@hooks.register('register_rich_text_features')
def register_strikethrough_feature(features):
    """
    Registering the `strikethrough` feature, which uses the `STRIKETHROUGH` Draft.js inline style type,
    and is stored as HTML with an `<s>` tag.
    """
    feature_name = 'strikethrough'
    type_ = 'STRIKETHROUGH'
    tag = 's'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'S',
        'description': 'Strikethrough',
        # This isn’t even required – Draftail has predefined styles for STRIKETHROUGH.
        'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule(
        'contentstate', feature_name, db_conversion)


@register_setting
class GeneralSettings(BaseSetting):
    site_author = models.TextField(
        max_length=127,
        blank=True, null=True)
    site_author_link = models.URLField(
        blank=True, null=True)
    pagination_count = models.PositiveIntegerField(
        default=10,
        help_text="Number of posts to display per page on index pages")
    disqus = models.CharField(
        max_length=127,
        null=True, blank=True,
        help_text="Site name on Disqus. Comments will only appear if this is provided.")
    google_analytics_id = models.CharField(
        max_length=127,
        blank=True, null=True,
        help_text='Google Analytics Tracking ID')

    panels = [
        FieldPanel('site_author'),
        FieldPanel('site_author_link'),
        FieldPanel('pagination_count'),
        FieldPanel('disqus'),
        FieldPanel('google_analytics_id'),
    ]
