from django.db import models
from core.validators import ENGLISH_REGEX_VALIDATOR


class AbstractBaseModel(models.Model):
    code = models.CharField("کد", max_length=18, unique=True, validators=[ENGLISH_REGEX_VALIDATOR])
    title = models.CharField("عنوان", max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AbstactDescriptionBaseModel(models.Model):
    code = models.CharField("کد", max_length=18, unique=True, validators=[ENGLISH_REGEX_VALIDATOR])
    description = models.TextField("توضیحات", max_length=200, null=False, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        abstract = True
