from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from .enums import RoleCodes
from django.db.transaction import commit


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        try:
            grades = extra_fields['grades']
            del extra_fields['grades']
        except:
            pass
        user = self.model(username=username, **extra_fields)
        password = make_password(str(password))
        user.password = password
        if user.gender is None:
            user.gender = True
        try:
            user.role
        except ObjectDoesNotExist:
            role = apps.get_model(app_label='accounts', model_name='Role')
            if user.is_superuser:
                user.role = role.objects.get(code=RoleCodes.ADMIN.value)
            else:
                user.role = role.objects.get(code=RoleCodes.STUDENT.value)
        user.set_default_avatar()
        user.save(using=self._db)
        try:
            if grades:
                user.grades.add(*grades)
                user.save(using=self._db)
        except:
            pass
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)

# not working :(((
# class TeacherUserManager(UserManager):
#     def get_queryset(self):
#         return super(TeacherUserManager, self).get_queryset().filter(role__code=RoleCodes.TEACHER.value)