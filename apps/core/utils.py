from django.core.mail import EmailMessage

class SendEmail:
    """
    to send email
    """
    @staticmethod
    def email(data):
        mail = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        mail.send()
