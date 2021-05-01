from time import sleep

from celery import shared_task
from django.core.mail import EmailMessage



@shared_task
def email(data):
    sleep(10)
    mail = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        to=[data['to_email']],
    )
    print(mail)
