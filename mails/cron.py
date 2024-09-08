from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)


def daily_email_task():
    logger.info("Начало выполнения задачи по отправке писем")
    call_command('send_emails')
    logger.info("Задача по отправке писем завершена")


def weekly_email_task():
    logger.info("Начало выполнения задачи по отправке писем")
    call_command('send_emails')
    logger.info("Задача по отправке писем завершена")


def monthly_email_task():
    logger.info("Начало выполнения задачи по отправке писем")
    call_command('send_emails')
    logger.info("Задача по отправке писем завершена")
