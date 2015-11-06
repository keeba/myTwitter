# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('follower', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='follower')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='follower',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='user',
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
    ]
