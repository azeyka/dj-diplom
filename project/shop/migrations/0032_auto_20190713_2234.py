# Generated by Django 2.1.3 on 2019-07-13 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_odereditem_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='odereditem',
            options={'verbose_name_plural': 'Заказанные товары'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='paginator_page',
        ),
    ]
