# vim:fileencoding=utf8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

import twitter

from core import utils

class Account(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=32)
    post_default = models.BooleanField(default=False)
    ctime = models.DateTimeField(default=datetime.now)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'アカウント'
        verbose_name_plural = u'アカウント'
        ordering = ('-post_default', '-ctime')

class MessageManager(models.Manager):
    def post_message(self, account, content):
        api = twitter.Api(
            username=account.username,
            password=account.password
        )
        timeline = api.PostUpdate(content)
        message = Message.objects.create(
            message_id=str(timeline.id),
            username=timeline.user.screen_name,
            content=timeline.text,
            ctime = utils.offset_timezone(datetime.strptime(
                timeline.created_at,
                '%a %b %d %H:%M:%S +0000 %Y'
            ))
        )
        message.followers.add(account)
        

class Message(models.Model):
    followers = models.ManyToManyField(Account, related_name='followers', blank=True)
    reply_to = models.ManyToManyField(Account, related_name='reply_to', blank=True)
    message_id = models.CharField(max_length=20, unique=True, db_index=True)
    username = models.CharField(max_length=128, db_index=True)
    is_direct = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)
    content = models.CharField(max_length=200)
    ctime = models.DateTimeField(default=datetime.now)

    objects = MessageManager()

    class Meta:
        verbose_name = u'メッセージ'
        verbose_name_plural = u'メッセージ'
        ordering = ('-ctime',)
