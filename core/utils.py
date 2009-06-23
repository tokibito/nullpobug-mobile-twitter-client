from pytz import timezone

from django.conf import settings

TZ = timezone(settings.TIME_ZONE)

def offset_timezone(d):
    return d + TZ.utcoffset('')
