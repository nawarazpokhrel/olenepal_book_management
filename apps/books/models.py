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
        unique=True,
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
    number_of_days_issued = models.DurationField(null=True, blank=True)

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
        if self.date_borrowed.day > datetime.today().day:
            raise DjangoValidationError(
                {'date_borrowed': _('Book cannot be borrowed from past date')})

        # Rule 3. If return date is smaller that borrowed date
        if self.return_date < self.date_borrowed:
            raise DjangoValidationError(
                {'return_date': _('Return date must be not be in past')})

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.book.available_books -= 1
            self.book.save()
            self.number_of_days_issued = self.return_date.date() - self.date_borrowed.date()
            super(BookBorrow, self).save(*args, **kwargs)

    def __str__(self):
        return self.book.name + " Borrowed by " + str(self.user.username)


class BookReturn(BaseModel):
    book_borrowed = models.OneToOneField(
        BookBorrow,
        on_delete=models.CASCADE
    )
    returned_date = models.DateTimeField()
    actual_issued_days = models.DurationField(null=True, blank=True)
    fine_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        default_permissions = ()

    def clean(self):
        # Rule 1. If return date is in past
        if not self.returned_date.date() > datetime.today().date():
            raise DjangoValidationError(
                {'returned_date': _('Return cannot be borrowed from past date')})

        # Rule 2. If return date smaller than date borrowed
        if self.returned_date < self.book_borrowed.date_borrowed:
            raise DjangoValidationError(
                {'returned_date': _('Returned date must be not be ahead of borrowed')})

    def save(self, *args, **kwargs):
        # If the operation is only adding
        if self._state.adding:
            # calculating days issued
            self.actual_days_issued_days = self.returned_date.date() - self.book_borrowed.date_borrowed.date()
            # if actual returned date is greater than return date
            print(self.actual_days_issued_days)
            if self.returned_date > self.book_borrowed.return_date:
                # calculate fine amount
                self.fine_amount = (self.actual_days_issued_days.days - self.book_borrowed.number_of_days_issued.days
                                    ) * 10
            super(BookReturn, self).save(*args, **kwargs)

    def __str__(self):
        return self.book_borrowed.book.name
