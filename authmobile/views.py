# vim:fileencoding=utf8
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from authmobile.models import MobileUser

def login_easy(request):
    """
    かんたんログイン
    """
    if request.agent.is_nonmobile():
        return HttpResponseBadRequest(u'モバイル端末でアクセスしてください')

    # サブスクライバーIDを取得
    if request.agent.is_docomo():
        guid = request.agent.guid
    else:
        guid = request.agent.serialnumber

    user = authenticate(subscriber_id=guid)
    if not user:
        return direct_to_template(request, 'authmobile/error.html', extra_context={
            'message': u'ユーザが見つかりません。',
        })
    login(request, user)
    return HttpResponseRedirect(reverse('site_index'))
