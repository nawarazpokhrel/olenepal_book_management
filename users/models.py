from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from shortuuidfield import ShortUUIDField

from users import validators


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for Management"""
    username_validator = UnicodeUsernameValidator()

    id = ShortUUIDField(
        primary_key=True,
        auto=True,
        editable=False,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(
        max_length=100,
        validators=[validators.validate_full_name]
    )
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[validators.validate_phone_number]
    )
    is_member = models.BooleanField(
        _('member'),
        help_text=_(
            'Designates whether this user should be treated as member. '
        ),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_librarian = models.BooleanField(
        _('librarian status'),
        default=False,
        help_text=_('Designates whether the user is librarian.'),
    )
    is_student = models.BooleanField(
        _('student status'),
        default=False,
        help_text=_('Designates whether the user is student.'),
    )

    is_verified = models.BooleanField(
        _('verification status'),
        default=False,
        help_text=_('Designates whether the user is verified via email or not.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.fullname

    # @property
    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }

    # @property
    # def user_type(self):
    #     if self.is_superuser:
    #         return UserType.super_user
    #     elif self.is_teacher:
    #         return UserType.teacher_user
    #     elif self.is_student:
    #         return UserType.student_user
    #     else:
    #         return UserType.librarian_user
