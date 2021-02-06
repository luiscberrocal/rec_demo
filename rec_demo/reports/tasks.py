from celery import shared_task

from .utils import generate_transaction_report


@shared_task
def create_transaction_report_task(**kwargs):
    url = generate_transaction_report(**kwargs)
    return url