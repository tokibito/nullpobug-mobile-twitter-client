from settings import *

def remove_from_list(target, item):
    if item in target:
        target.remove(item)
    return target

MIDDLEWARE_CLASSES = remove_from_list(list(MIDDLEWARE_CLASSES), 'bpmobile.middleware.BPMobileDenyBogusIP')

#INSTALLED_APPS = list(INSTALLED_APPS)
#INSTALLED_APPS.append('django_extensions')
