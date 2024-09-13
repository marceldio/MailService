from django.core.management import call_command
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)


def should_send_mailing(mailing, now):
    """Функция проверяет, нужно ли отправить данную рассылку в данный момент."""
    if mailing.frequency == "daily":
        return mailing.scheduled_at.time() == now.time()
    elif mailing.frequency == "weekly":
        return (
            mailing.scheduled_at.time() == now.time()
            and mailing.scheduled_at.weekday() == now.weekday()
        )
    elif mailing.frequency == "monthly":
        return (
            mailing.scheduled_at.time() == now.time()
            and mailing.scheduled_at.day == now.day
        )
    return False


def periodic_email_task():
    """Функция для периодической проверки и отправки рассылок"""
    logger.info("Начало выполнения периодической задачи по отправке писем")
    check_pending_mailings()
    logger.info("Периодическая задача по отправке писем завершена")


def check_pending_mailings():
    from mails.models import Sending
    logger.info("Начало проверки активных рассылок")
    now = timezone.now()
    logger.info(f"Проверка активных рассылок на {now}")

    pending_mailings = Sending.objects.filter(
        is_active=True,
        scheduled_at=timezone.now(),
        # scheduled_at__lte=timezone.now(),
    )

    for mailing in pending_mailings:
        if should_send_mailing(mailing, now):
            logger.info(f"Запуск команды отправки рассылки с ID {mailing.id}")
            call_command("send_emails")
            logger.info(f"Команда отправки рассылки с ID {mailing.id} завершена")
    logger.info("Проверка активных рассылок завершена")
