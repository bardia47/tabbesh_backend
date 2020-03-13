from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True
    

    def _create_user(self,username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username=username
        password = make_password(password)
        user.password=password
        if user.gender is None:
            user.gender = True
        try:
            user.role
        except ObjectDoesNotExist:
            role = apps.get_model(app_label='accounts', model_name='Role')
            user.role = role.objects.get(code='1')

        user.save(using=self._db)
        return user

    def create_user(self,username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username,email, password, **extra_fields)

    def create_superuser(self, username,email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username,email, password, **extra_fields)