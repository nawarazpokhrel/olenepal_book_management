from templated_mail.mail import BaseEmailMessage


class ConfirmationEmail(BaseEmailMessage):
    template_name = 'email/created_email.html'


class BookUpdateEmail(BaseEmailMessage):
    template_name = 'email/book_updated_email.html'


class BookDeletedEmail(BaseEmailMessage):
    template_name = 'email/book_deleted_email.html'


class BookCreatedEmail(BaseEmailMessage):
    template_name = 'email/book_created_email.html'
