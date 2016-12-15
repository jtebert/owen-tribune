# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent

from django import template
from blog.models import ArticleIndexPage

register = template.Library()

@register.inclusion_tag('navbar.html', takes_context=True)
def subject_menu(context, current_page):
    parent = context['request'].site.root_page
    menuitems = parent.get_children().type(ArticleIndexPage).filter(
        live=True,
    )
    return {
        'menuitems': menuitems,
        'current_page': current_page,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }