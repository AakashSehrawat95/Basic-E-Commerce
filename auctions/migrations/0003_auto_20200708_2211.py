# Generated by Django 3.0.7 on 2020-07-08 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 8, 22, 11, 18, 716869)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to='media'),
        ),
    ]
