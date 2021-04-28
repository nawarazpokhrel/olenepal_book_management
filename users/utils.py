import enum

from django.core.mail import EmailMessage


class UserType(enum.Enum):
    """
    This class was created to define user type
    """
    normal_user = 1
    library_user = 2
    super_user = 3


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
