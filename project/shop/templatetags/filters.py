from django import template

register = template.Library()

@register.filter
def get_page(paginator, page_num):
    return paginator.get_page(page_num)

@register.filter
def convert_stars(stars):
    return '★'*stars

@register.filter
def get_from_session(session, id):
    return session[id]