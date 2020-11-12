from django.core.validators import RegexValidator


ENGLISH_REGEX_VALIDATOR_MESSAGE = 'تنها باید شامل حروف و اعداد انگلیسی باشد.'
ENGLISH_REGEX_VALIDATOR = RegexValidator(regex='^[a-zA-Z0-9]+$', message=ENGLISH_REGEX_VALIDATOR_MESSAGE)
