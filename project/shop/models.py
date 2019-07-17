from django.db import models
from pytils.translit import slugify
from django.core.paginator import Paginator
from django.contrib.auth.models import AbstractUser


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    section = models.ForeignKey('Section', verbose_name='Раздел', on_delete=models.SET_NULL, null=True)
    img = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание товара', null=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    parent = models.ForeignKey('Section', verbose_name='Родительский раздел', on_delete=models.SET_NULL,
                               parent_link=True, null=True, blank=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
    
    def __str__(self):
        return self.name
    
    def subsections(self):
        return Section.objects.all().filter(parent=self)
    
    def subsection_count(self):
        return Section.objects.all().filter(parent=self).count()
    
    def items(self):
        return Item.objects.filter(section=self)
    
    def items_count(self):
        return Item.objects.filter(section=self).count()
    
    def paginator(self):
        return Paginator(self.items(), 3)


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    section = models.ForeignKey('Section', verbose_name='Показать товары из подраздела',
                                on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title
    
    def items(self):
        return Item.objects.filter(section=self.section)
    

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    name = models.CharField(max_length=20, verbose_name='Имя')
    text = models.TextField(verbose_name='Текст')
    stars = models.IntegerField(verbose_name='Количество звезд')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.username
    
    def cart(self):
        return Cart.objects.filter(user=self)
        
class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    
    class Meta:
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.item.name} ({self.quantity}шт.)'

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Заказчик', null=True)
    order_time = models.DateTimeField(verbose_name='Время заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id} от {self.order_time.date()}'
    
    def order_num(self):
        return f'Заказ №{self.id}'
    
    def items_count(self):
        return self.odereditem_set.count()
    
class OderedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    
    class Meta:
        verbose_name_plural = 'Заказанные товары'
    
    def __str__(self):
        return self.item.name
    
    def count(self):
        return self.quantity