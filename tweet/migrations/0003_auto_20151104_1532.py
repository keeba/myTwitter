# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0002_auto_20151104_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followee',
            name='user',
        ),
        migrations.AddField(
            model_name='followee',
            name='followee',
            field=models.ForeignKey(default=1, related_name='followee', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
