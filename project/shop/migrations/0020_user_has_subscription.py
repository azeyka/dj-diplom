# Generated by Django 2.1.3 on 2019-07-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_subscription',
            field=models.BooleanField(default=False),
        ),
    ]
