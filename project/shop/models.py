from django.db import models
from pytils.translit import slugify
from django.core.paginator import Paginator
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    subsection = models.ForeignKey('Subsection', verbose_name='Подраздел', on_delete=models.SET_NULL, null=True)
    img = models.ImageField(verbose_name='Изображение', upload_to='/images')
    description = models.TextField(verbose_name='Описание товара', null=True)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
    
    def __str__(self):
        return self.name
    
    def subsection_count(self):
        return Subsection.objects.filter(section=self).count()
    
    def items_count(self):
        return Item.objects.filter(subsection__section=self).count()

class Subsection(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(null=True)
    section = models.ForeignKey('Section', verbose_name='Раздел', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Подраздел'
        verbose_name_plural = 'Подразделы'
    
    def __str__(self):
        return self.name
    
    def items_count(self):
        return Item.objects.filter(subsection=self).count()
    
    def items(self):
        return Item.objects.filter(subsection=self)
    
    def paginator(self):
        return Paginator(self.items(), 3)

class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    subsection = models.ForeignKey('Subsection', verbose_name='Показать товары из секции', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title
    
    def items(self):
        return Item.objects.filter(subsection=self.subsection)
    
    def paginator(self):
        return self.subsection.paginator()

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    name = models.CharField(max_length=20, verbose_name='Имя')
    text = models.TextField(verbose_name='Текст')
    stars = models.IntegerField(verbose_name='Количество звезд')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Customer(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user.username
    
    def cart(self):
        return Cart.objects.filter(user=self)
    
class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Пользователь')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    
    class Meta:
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.item.name} ({self.quantity}шт.)'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Заказчик')
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