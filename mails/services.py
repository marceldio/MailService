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
    cache.set(key, sendings)
    return sendings


def get_mails_from_cache():
    if not CACHE_ENABLED:
        return Maill.objects.all()
    key = "maill_list"
    mails = cache.get(key)
    if mails is not None:
        return mails
    mails = Maill.objects.all()
    cache.set(key, mails)
    return mails


def get_recipients_from_cache():
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients
