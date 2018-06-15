from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.core.models import Page
from blog.models import ArticlePage
from wagtail.search.models import Query


def search(request):
    search_query = request.GET.get('query', None)

    # Search
    if search_query:
        search_results = ArticlePage.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = ArticlePage.objects.none()

    # Pagination
    page = request.GET.get('page')
    page_size = 10
    from home.models import GeneralSettings
    if GeneralSettings.for_site(request.site).pagination_count:
        page_size = GeneralSettings.for_site(request.site).pagination_count

    if page_size is not None:
        paginator = Paginator(search_results, page_size)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
