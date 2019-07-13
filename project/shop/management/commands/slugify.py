from django.core.management.base import BaseCommand
from pytils.translit import slugify

from shop.models import Item, Section, Subsection


class Command(BaseCommand):
    models_to_slugify = [Item, Section, Subsection]

    def handle(self, *args, **options):
        for model in self.models_to_slugify:
          elements = model.objects.all()
          for element in elements:
            slug = slugify(element.name)
            element.slug = slug
            element.save()