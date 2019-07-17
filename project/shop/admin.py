from django.contrib import admin
from django.forms import BaseInlineFormSet

from shop.models import Item, Section, Article, Order, OderedItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'section']
    list_filter = ['section']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'items_count']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']

class OrdedItemInlineFormset(BaseInlineFormSet):
    pass

class OrdedItemInline(admin.TabularInline):
    model = OderedItem
    formset = OrdedItemInlineFormset
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['order_time']
    list_display = ['order_num', 'user', 'order_time', 'items_count']
    inlines = [OrdedItemInline]