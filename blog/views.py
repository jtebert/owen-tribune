from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from taggit.models import Tag

from blog.models import ArticlePage

from home.models import GeneralSettings


# Create your views here.


def tag_filter(request):
    tags = ArticlePage.tags.order_by('name')

    # ArticlePage.objects.live().filter(tags__name__in=value['tags'])

    # Tag
    tag = request.GET.get('tag')
    if tag:
        articles = ArticlePage.objects.live().filter(tags__name=tag)
    else:
        articles = ArticlePage.objects.none()

    # Pagination
    page = request.GET.get('page')
    page_size = 10
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

    return render(request, 'blog/tag_filter.html', {
        'tag_query': tag,
        'tags': tags,
        'filter_results': articles,
    })


def articles(request):
    # Show all articles, sorted newest to oldest
    articles = ArticlePage.objects.live().order_by('-date')

    # Pagination
    page = request.GET.get('page')
    page_size = 10
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

    return render(request, 'blog/articles.html', {
        'articles': articles,
    })
