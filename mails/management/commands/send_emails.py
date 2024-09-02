from django.core.management.base import BaseCommand
from django.conf import settings
import pytz
from mails.models import Sending


class Command(BaseCommand):
    help = "Отправка рассылки по расписанию"

    def handle(self, *args, **kwargs):
        self.send_mailing()

    def send_mailing(self):
        zone = pytz.timezone(settings.TIME_ZONE)
        self.stdout.write(self.style.SUCCESS(f"Timezone set to {zone}"))
        mailings = Sending.objects.filter(status="launched")
        self.stdout.write(
            self.style.SUCCESS(f"Найдено {mailings.count()} активных рассылки")
        )

        for mailing in mailings:
            # Логика отправки письма
            try:
                mailing.send()
                self.stdout.write(
                    self.style.SUCCESS(f"Рассылка отправлена на {mailing.id}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка отправки на {mailing.id}: {str(e)}")
                )
