from django.core.management.base import BaseCommand
from django.conf import settings
import pytz
from mails.models import Sending


class Command(BaseCommand):
    help = 'Отправка рассылки по расписанию'

    def handle(self, *args, **kwargs):
        self.send_mailing()

    def send_mailing(self):
        zone = pytz.timezone(settings.TIME_ZONE)
        # Ваш код рассылки
        mailings = Sending.objects.filter(status='active')
        for mailing in mailings:
            # Логика отправки письма
            mailing.send()
            self.stdout.write(self.style.SUCCESS(f'Рассылка отправлена на {mailing.email}'))
