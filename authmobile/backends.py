from django.contrib.auth.models import User

from authmobile.models import MobileUser

class MobileSubscriberBackend:
    def authenticate(self, username=None, password=None, subscriber_id=None):
        mobileuser = MobileUser.objects.get_by_subscriber_id(subscriber_id=subscriber_id)
        if mobileuser:
            return mobileuser.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
