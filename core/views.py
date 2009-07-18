import socket
socket.setdefaulttimeout(30)
from datetime import datetime

from pytz import timezone

import twitter

from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import IntegrityError

from authmobile.models import MobileUser

from core.models import Account, Message
from core.forms import PostMessageForm

TZ = timezone(settings.TIME_ZONE)

NUM_OF_MESSAGES_BY_PAGE = 30

@login_required
def index(request):
    account_ids = list(Account.objects.filter(user=request.user).values_list('id', flat=True))
    messages = Message.objects.filter(followers__id__in=account_ids)[:NUM_OF_MESSAGES_BY_PAGE]
    return direct_to_template(request, 'core/index.html', extra_context={
        'message_list': messages,
        'form': PostMessageForm(),
    })

@login_required
def post_message(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('site_index'))
    form = PostMessageForm(request.POST)
    if form.is_valid():
        accounts = Account.objects.filter(user=request.user)[:1]
        if accounts:
            api = twitter.Api(
                username=accounts[0].username,
                password=accounts[0].password
            )
            timeline = api.PostUpdate(form.cleaned_data['message'])
            message = Message.objects.create(
                message_id=str(timeline.id),
                username=timeline.user.screen_name,
                content=timeline.text,
                ctime = datetime.strptime(
                    timeline.created_at,
                    '%a %b %d %H:%M:%S +0000 %Y'
                ) + TZ.utcoffset('')
            )
            message.followers.add(accounts[0])
    return HttpResponseRedirect(reverse('site_index'))

@login_required
def fetch_friends_timeline(request):
    """
    fetch messages and redirect index.
    """
    for account in Account.objects.filter(user=request.user):
        try:
            api = twitter.Api(
                username=account.username,
                password=account.password
            )
            for timeline in api.GetFriendsTimeline():
                try:
                    message = Message.objects.create(
                        message_id=str(timeline.id),
                        username=timeline.user.screen_name,
                        content=timeline.text,
                        ctime = datetime.strptime(
                            timeline.created_at,
                            '%a %b %d %H:%M:%S +0000 %Y'
                        ) + TZ.utcoffset('')
                    )
                except IntegrityError:
                    message = Message.objects.get(message_id=str(timeline.id))
                message.followers.add(account)
        except:
            pass
    return HttpResponseRedirect(reverse('site_index'))

@login_required
def config(request):
    try:
        mobileuser = request.user.mobileuser
    except:
        mobileuser = None
    return direct_to_template(request, 'core/config.html', extra_context={
        'mobileuser': mobileuser, 
    })

@login_required
def config_login_easy(request):
    agent = request.agent
    if not agent.is_nonmobile():
        if agent.is_docomo():
            subscriber_id = agent.guid
        else:
            subscriber_id = agent.serialnumber
        try:
            MobileUser.objects.reset_subscriber_id(subscriber_id)
            mobileuser = MobileUser.objects.get(user=request.user)
            mobileuser.subscriber_id = subscriber_id
            mobileuser.save()
        except MobileUser.DoesNotExist:
            mobileuser = MobileUser.objects.create(user=request.user, subscriber_id=subscriber_id)
    return HttpResponseRedirect(reverse('core_config'))
