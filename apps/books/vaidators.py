from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _

from apps.core.validators import WordValidator


@deconstructible
class NameValidator(WordValidator):
    """
    Allows to have 4 word  name
    """
    message = _('Enter a valid  name.')
    number_of_word = 4


@deconstructible
class AddressValidator(WordValidator):
    """
    Allows to have 25 word address
    """
    message = _('Enter a valid address.')
    number_of_word = 25
    word_length = 2
    one_word_regex = _lazy_re_compile(
        r'^[a-zA-Z0-9]+$'
    )
    multi_word_regex = _lazy_re_compile(
        r'^[a-zA-Z0-9-\s]+$'
    )


# Books and Author
validate_name = NameValidator()
validate_address = AddressValidator()
