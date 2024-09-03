from mails.models import Sending, Maill, Recipient
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_sendings_from_cache():
    if not CACHE_ENABLED:
        return Sending.objects.all()
    key = "sending_list"
    sendings = cache.get(key)
    if sendings is not None:
        return sendings
    sendings = Sending.objects.all()
    cache.set(key, sendings, timeout=60)
    return sendings


def get_mails_from_cache(self):
    if not CACHE_ENABLED:
        # return Maill.objects.all()
        return Maill.objects.filter(author=self.request.user)
    key = "maill_list"
    mails = cache.get(key)
    if mails is not None:
        return mails
    # mails = Maill.objects.all()
    mails = Maill.objects.filter(author=self.request.user)
    cache.set(key, mails, timeout=60)
    return mails


def get_recipients_from_cache(self):
    if not CACHE_ENABLED:
        # return Recipient.objects.all()
        return Recipient.objects.filter(
            owner=self.request.user
        )  # для текущего пользователя
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    # recipients = Recipient.objects.all()
    recipients = Recipient.objects.filter(owner=self.request.user)
    cache.set(key, recipients, timeout=60)
    return recipients
