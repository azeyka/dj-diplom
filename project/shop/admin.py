from django.contrib import admin
from django.forms import BaseInlineFormSet

from shop.models import Item, Section, Subsection, Article, Review, Customer, Cart, Order, OderedItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subsection']
    list_filter = ['subsection__section', 'subsection']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'subsection_count', 'items_count']

@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'items_count']
  
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'stars']
    
class CartInlineFormset(BaseInlineFormSet):
    pass

class CartInline(admin.TabularInline):
    model = Cart
    formset = CartInlineFormset
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [CartInline]

class OrdedItemInlineFormset(BaseInlineFormSet):
    pass

class OrdedItemInline(admin.TabularInline):
    model = OderedItem
    formset = OrdedItemInlineFormset
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['order_time']
    list_display = ['order_num', 'customer', 'order_time', 'items_count']
    inlines = [OrdedItemInline]