from celery import shared_task
from django.contrib import messages
from django.utils import timezone


@shared_task()
def remind():
    from .models import ClassRecord
    active_records = ClassRecord.objects.filter(exit_time__isnull=True)
    for record in active_records:
        messages.info(record.teacher_name, 'you are still in class, dont forget to log_out')
