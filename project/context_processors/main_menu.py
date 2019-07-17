from django.template.context_processors import request
from shop.models import Item, Section


def menu(request):
    return {
        'all_sections': Section.objects.all().order_by('name'),
        'all_items': Item.objects.all().order_by('name'),
    }