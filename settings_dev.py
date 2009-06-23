from settings import *

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.remove('bpmobile.middleware.BPMobileDenyBogusIP')

#INSTALLED_APPS = list(INSTALLED_APPS)
#INSTALLED_APPS.append('django_extensions')
