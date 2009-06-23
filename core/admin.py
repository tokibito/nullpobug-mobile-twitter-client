from django.contrib import admin

from core.models import Account, Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'username', 'content', 'ctime')

admin.site.register(Account)
admin.site.register(Message, MessageAdmin)
