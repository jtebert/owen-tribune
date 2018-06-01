from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
from wagtail.core import blocks
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

# TODO: Add snippets for top/bottom menus: http://jordijoan.me/simple-orderable-menus-wagtail/

md_format_help = 'This text will be formatted with markdown.'


'''
@register_snippet
class SubjectSnippet(models.Model):
    """
    Identifies the different subjects under which to categorize articles
    """
    subject_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject_name



@register_snippet
class AuthorSnippet(models.Model):
    """
    Create a profile for each author, which will be paired with the articles they write
    """
    # NOT USED NOW
    author_name = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL)
    portrait = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = models.TextField(max_length=800, null=True)
    homepage = models.URLField(blank=True)

    panels = [
        FieldPanel('author_name'),
        FieldPanel('user'),
        FieldPanel('bio'),
        ImageChooserPanel('portrait'),
        FieldPanel('homepage'),
    ]

    def __unicode__(self):
        return self.author_name

    class Meta:
        verbose_name = "Author"
'''

class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(help_text='This will override the default caption.'+md_format_help,
                               blank=True, null=True, required=False)

    class Meta:
        icon = 'image'
        template = 'blog/captioned_image_block.html'
        label = 'Image'


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()

    class Meta:
        icon = 'openquote'
        template = 'blog/quote.html'

'''
class CodeBlock(blocks.TextBlock):
    class Meta:
        template = 'blog/code_blog.html'
        icon = 'code'
        label = 'Code'
'''


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('ArticlePage', related_name='tagged_items')


class ArticlePage(Page):
    parent_page_types = ["ArticleIndexPage",]
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
        max_length=250,
        help_text='This will only appear in article previews, not with the full article.'+md_format_help)
    body = StreamField([
        ('text', blocks.TextBlock(icon='pilcrow', help_text=md_format_help)),
        ('image', CaptionedImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('pull_quote', QuoteBlock()),
        ('table', TableBlock(template='blog/table_block.html')),
    ])
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    content_panels = Page.content_panels + [
        PageChooserPanel('author', ),
        FieldPanel('date'),
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        #index.SearchField('tags__name'),
    ]

    class Meta:
        verbose_name = "Article"

    def __unicode__(self):
        return self.title

    def subject(self):
        # Find closest ancestor which is article index page
        return self.get_ancestors().type(ArticleIndexPage).last()

    """def subject(self):
        # TODO: Replace/remove
        subject = ArticleIndexPage.objects.ancestor_of(self).last().subject
        if subject is not None:
            return subject
        else:
            return ""
    """

    """
    def all_subjects(self):
        # TODO: Replace/remove
        subjects = []
        for s in SubjectPage.objects.all():
            subjects.append(ArticleIndexPage.objects.filter(subject=s)[0])
        return subjects
    """


class SourceLink(models.Model):
    title = models.TextField(max_length=1023, help_text=md_format_help+"Use a standard citation format.", blank=True, null=True)
    url = models.URLField('Link to Source', blank=True, null=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
    ]

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class ArticleIndexRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('ArticleIndexPage', related_name='related_links')


class ArticleIndexPage(Page):
    subpage_types = ['ArticlePage']

    intro = models.TextField(
        blank=True,
        help_text=md_format_help)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        # InlinePanel('related_links', label="Related links"),
    ]

    class Meta:
        verbose_name = 'Subject Section'

    def get_context(self, request, *args, **kwargs):
        context = super(ArticleIndexPage, self).get_context(
            request, *args, **kwargs)
        articles = self.articles()

        # Tags
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__name=tag)

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
            articles = articles.filter(Q(subject_1=subject_filter) | Q(subject_2=subject_filter))
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


'''
class SubjectCategoryPage(Page):
    parent_page_types = ['SubjectIndexPage']
    subpage_types = ['SubjectPage']

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Subject Category'


class SubjectIndexPage(Page):
    subpage_types = ['SubjectCategoryPage']

    intro = models.TextField(
        blank=True,
        help_text=md_format_help)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def list_subjects(self):
        """
        List all authors
        :return:
        """
        return SubjectPage.objects.all()
'''


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
        return ArticlePage.objects.live().filter(author=self).order_by('title')

    def __unicode__(self):
        return self.title


class AuthorIndexPage(Page):
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
