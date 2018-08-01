from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (FieldPanel,
                                         InlinePanel,
                                         MultiFieldPanel,
                                         PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks, hooks
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmedia.blocks import AbstractMediaChooserBlock

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler


md_format_help = 'This text will be formatted with markdown.'
DEFAULT_RICHTEXT_FEATURES = [
    'h2', 'h3', 'h4', 'h5',
    'bold', 'italic', 'strikethrough', 'code',
    'ol', 'ul',
    'hr',
    'link',
    'document-link',
]


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(help_text='This will override the default caption.'+md_format_help,
                               blank=True, null=True, required=False)
    image_format = blocks.ChoiceBlock(choices=[
        ('full-width', 'Full width'),
        ('centered', 'Medium centered'),
        ('left', 'Left-aligned'),
        ('right', 'Right-aligned'),
    ])

    class Meta:
        icon = 'image'
        template = 'blog/captioned_image_block.html'
        label = 'Captioned Image'


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()

    class Meta:
        icon = 'openquote'
        template = 'blog/quote.html'


class MediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = 'blog/video_block.html'
        else:
            player_code = 'blog/audio_block.html'

        if not context:
            context = {}
        context['media'] = value
        return render_to_string(player_code, context)


class OptionsMediaBlock(blocks.StructBlock):
    media = MediaBlock()
    show_controls = blocks.BooleanBlock(required=False, default=True)
    autoplay = blocks.BooleanBlock(required=False)
    loop = blocks.BooleanBlock(required=False)
    muted = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'media'
        template = 'blog/media_block.html'


class CodeBlock(blocks.StructBlock):
    code = blocks.TextBlock()
    language = blocks.CharBlock(required=False)
    show_line_numbers = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        template = 'blog/code_block.html'
        icon = 'code'
        label = 'Code'


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('ArticlePage', related_name='tagged_items')


class ArticlePage(Page):
    parent_page_types = ["ArticleIndexPage", ]
    subpage_types = []

    author = models.ForeignKey(
        'AuthorPage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    main_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField("Post date")
    intro = models.TextField(
        max_length=480,
        help_text='This will only appear in article previews, not with the full article.'+md_format_help)
    body = StreamField([
        ('text', blocks.RichTextBlock(features=DEFAULT_RICHTEXT_FEATURES)),
        ('captioned_image', CaptionedImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('pull_quote', QuoteBlock()),
        ('table', TableBlock(template='blog/table_block.html')),
        ('media', OptionsMediaBlock()),
        ('code', CodeBlock()),
    ])
    notes = models.TextField(
        null=True, blank=True,
        help_text="This text will not appear on the page.")
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    content_panels = Page.content_panels + [
        PageChooserPanel('author', ),
        FieldPanel('date'),
        ImageChooserPanel('main_image'),
        InlinePanel('article_audiences', label='Audiences'),
        FieldPanel('tags'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        FieldPanel('notes'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        # index.SearchField('tags__name'),
    ]

    class Meta:
        verbose_name = "Article"

    def __unicode__(self):
        return self.title

    def subject(self):
        # Find closest ancestor which is article index page
        return self.get_ancestors().type(ArticleIndexPage).last()


class AudienceIndexPage(Page):
    #parent_page_types = [home.models.HomePage, ]
    subpage_types = ['AudiencePage']

    class Meta:
        verbose_name = 'Audiences'

    def get_context(self, request, *args, **kwargs):
        context = super(AudienceIndexPage, self).get_context(
            request, *args, **kwargs)
        audiences = self.get_children().live().order_by('title')
        context['audiences'] = audiences
        return context

    def articles(self, audience_filter=None):
        """
        Return all articles if no audience specified, otherwise only those from that Audience
        :param audience_filter: str
        :return: QuerySet of Articles (I think)
        """
        articles = ArticlePage.objects.live().descendant_of(self)
        if audience_filter is not None:
            articles = articles.filter(audience__name=audience_filter)
        articles = articles.order_by('-date')
        return articles


class AudiencePage(Page):
    parent_page_types = ['AudienceIndexPage', ]
    subpage_types = []

    class Meta:
        verbose_name = 'Audience'

    intro = models.TextField(
        max_length=480,
        blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(AudiencePage, self).get_context(
            request, *args, **kwargs)
        articles = ArticlePage.objects.live().filter(
            article_audiences__audience=self).order_by('-date')

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        from home.models import GeneralSettings
        if GeneralSettings.for_site(request.site).pagination_count:
            page_size = GeneralSettings.for_site(request.site).pagination_count

        if page_size is not None:
            paginator = Paginator(articles, page_size)
            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        return context

    def __unicode__(self):
        return self.title


class AudienceLink(Orderable):
    page = ParentalKey('ArticlePage', related_name='article_audiences')
    audience = models.ForeignKey(AudiencePage,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 )

    panels = [
        PageChooserPanel('audience')
    ]


class ArticleIndexPage(Page):
    subpage_types = ['ArticlePage']

    class Meta:
        verbose_name = 'Subject Section'

    def get_context(self, request, *args, **kwargs):
        context = super(ArticleIndexPage, self).get_context(
            request, *args, **kwargs)
        articles = self.articles()

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        from home.models import GeneralSettings
        if GeneralSettings.for_site(request.site).pagination_count:
            page_size = GeneralSettings.for_site(request.site).pagination_count

        if page_size is not None:
            paginator = Paginator(articles, page_size)
            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        return context

    def articles(self, subject_filter=None):
        """
        Return all articles if no subject specified, otherwise only those from that Subject
        :param subject_filter: Subject
        :return: QuerySet of Articles (I think)
        """
        articles = ArticlePage.objects.live().descendant_of(self)
        if subject_filter is not None:
            articles = articles.filter(
                Q(subject_1=subject_filter) | Q(subject_2=subject_filter))
        articles = articles.order_by('-date')
        return articles


class SubjectPage(Page):
    """
    Identifies the different subjects under which to categorize articles
    """
    parent_page_types = ['ArticleIndexPage']
    subpage_types = []

    description = models.TextField(
        max_length=800,
        null=True, blank=True,
        help_text=md_format_help)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Subject"


class AuthorPage(Page):
    parent_page_types = ['AuthorIndexPage']
    subpage_types = []

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL, )
    portrait = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_bio = models.TextField(
        max_length=800,
        null=True, blank=True,
        help_text='This text will appear at the end of articles.'+md_format_help)
    long_bio = models.TextField(
        null=True, blank=True,
        help_text='This text will appear on the author page.'+md_format_help)
    #personal_website = models.URLField(blank=True)
    twitter_handle = models.CharField(
        max_length=15,
        null=True, blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('user'),
        FieldPanel('short_bio'),
        FieldPanel('long_bio'),
        ImageChooserPanel('portrait'),
        FieldPanel('twitter_handle'),
    ]

    def author_articles(self):
        """
        Get all articles by this author
        :return: QuerySet of ArticlePages
        """
        return ArticlePage.objects.live().filter(author=self).order_by('-date')

    def __unicode__(self):
        return self.title


class AuthorIndexPage(Page):
    #parent_page_types = [HomePage, ]
    subpage_types = ['AuthorPage']

    intro = models.TextField(
        blank=True,
        help_text=md_format_help)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    class Meta:
        verbose_name = 'Authors List'

    def authors(self):
        """
        List all authors
        :return:
        """
        return AuthorPage.objects.all()

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(AuthorIndexPage, cls).can_create_at(parent) \
            and not cls.objects.exists()
