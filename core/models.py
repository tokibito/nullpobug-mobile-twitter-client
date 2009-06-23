# vim:fileencoding=utf8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

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

class Message(models.Model):
    followers = models.ManyToManyField(Account, related_name='followers')
    reply_to = models.ManyToManyField(Account, related_name='reply_to')
    message_id = models.CharField(max_length=20, unique=True, db_index=True)
    username = models.CharField(max_length=128, db_index=True)
    is_direct = models.BooleanField(default=False)
    content = models.CharField(max_length=200)
    ctime = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'メッセージ'
        verbose_name_plural = u'メッセージ'
        ordering = ('-ctime',)
