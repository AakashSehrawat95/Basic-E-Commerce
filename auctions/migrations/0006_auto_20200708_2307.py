# Generated by Django 3.0.7 on 2020-07-08 17:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200708_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 8, 17, 37, 42, 573896, tzinfo=utc)),
        ),
    ]
