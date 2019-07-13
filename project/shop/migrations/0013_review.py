# Generated by Django 2.1.3 on 2019-07-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя')),
                ('text', models.TextField(verbose_name='Текст')),
                ('stars', models.IntegerField(verbose_name='Количество звезд')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]