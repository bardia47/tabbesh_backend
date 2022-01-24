from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


ENGLISH_REGEX_VALIDATOR_MESSAGE = _("Must only contain English letters and numbers.")
ENGLISH_REGEX_VALIDATOR = RegexValidator(regex='^[a-zA-Z0-9]+$', message=ENGLISH_REGEX_VALIDATOR_MESSAGE)

CHAR_REGEX_VALIDATOR_MESSAGE = _("It should only contain English letters and numbers and special letters.")
CHAR_REGEX_VALIDATOR = RegexValidator(regex=r'^[\w.@+-]+$', message=CHAR_REGEX_VALIDATOR_MESSAGE)

PERSIAN_REGEX_VALIDATOR_MESSAGE = _("It should only contain Persian letters.")
PERSIAN_REGEX_VALIDATOR = RegexValidator(regex='^[\u0600-\u06FF\s]+$', message=PERSIAN_REGEX_VALIDATOR_MESSAGE)


PHONE_NUMBER_REGEX_VALIDATOR_MESSAGE = _("Phone number is not valid.")
PHONE_NUMBER_REGEX_VALIDATOR = RegexValidator(regex='^(\\+98|0)?9\d{9}$', message=PHONE_NUMBER_REGEX_VALIDATOR_MESSAGE)
