# Generated by Django 2.1.3 on 2019-07-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_article_subsection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AddField(
            model_name='article',
            name='paginator_page',
            field=models.IntegerField(default=1, verbose_name='Страница товаров'),
        ),
    ]
