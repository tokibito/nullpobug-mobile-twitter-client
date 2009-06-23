# vim:fileencoding=utf8
from django.db import models

from django.contrib.auth.models import User

class MobileUserManager(models.Manager):
    def get_by_subscriber_id(self, subscriber_id):
        try:
            return self.get(subscriber_id=subscriber_id)
        except MobileUser.DoesNotExist:
            pass

    def reset_subscriber_id(self, subscriber_id):
        mobileuser = self.get_by_subscriber_id(subscriber_id=subscriber_id)
        if mobileuser:
            mobileuser.subscriber_id = ''
            mobileuser.save()

class MobileUser(models.Model):
    """
    djangoのユーザにモバイルの情報を持たせる
    """
    user = models.OneToOneField(User)
    subscriber_id = models.CharField(u'サブスクライバーID', max_length=64, db_index=True)

    objects = MobileUserManager()

    class Meta:
        verbose_name = u'モバイルユーザ'
        verbose_name_plural = u'モバイルユーザ'
        db_table = 'mobile_user'
