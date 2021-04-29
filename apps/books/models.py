from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.books import vaidators
from apps.core.models import BaseModel
from apps.core.validators import PhoneNumberValidator

User = get_user_model()


class Publication(BaseModel):
    name = models.CharField(
        max_length=100,
        validators=[vaidators.validate_name],
        unique=True
    )
    address = models.CharField(
        max_length=100,
        validators=[vaidators.validate_address]
    )
    phone_number = models.CharField(
        max_length=10,
        validators=[PhoneNumberValidator],
        unique=True
    )

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class Author(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    address = models.CharField(
        max_length=100,
        validators=[vaidators.validate_address]
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE
    )

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.user.username


class Book(BaseModel):
    name = models.CharField(
        max_length=100,
        validators=[vaidators.validate_name],
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    edition = models.CharField(max_length=100)
    available_books = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    publication = models.ManyToManyField(Publication)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class BookBorrow(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField()
    return_date = models.DateTimeField()
    # fine_amount = models.PositiveIntegerField()
    number_of_days_issued = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = ()
        # Basically idea is to allow one user to allow borrow unique book
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'user'],
                name='unique book for user'
            )
        ]

    def clean(self):
        # Rule 1. If books are not available raise error
        if not self.book.available_books > 0:
            raise DjangoValidationError(
                {'book': _('There are no books available at the moment')})

        # Rule 2. If book borrowed date is in past
        if self.date_borrowed.day < datetime.today().day:
            raise DjangoValidationError(
                {'date_borrowed': _('Book cannot be borrowed from past date')})

        # Rule 3. If return date is smaller that borrowed date
        if self.return_date < self.date_borrowed:
            raise DjangoValidationError(
                {'return_date': _('Return date must be not be in past')})

    def save(self, *args, **kwargs):
        self.book.available_books = self.book.available_books - 1
        self.book.save()
        self.number_of_days_issued = self.return_date.day - self.date_borrowed.day
        super(BookBorrow, self).save(*args, **kwargs)

    def __str__(self):
        return self.book.name + " Borrowed by " + str(self.user.username)
