from django.contrib.auth.models import (
    BaseUserManager
)
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# TODO здесь должен быть менеджер для модели Юзера.
# TODO Поищите эту информацию в рекомендациях к проекту
class UserManager(BaseUserManager):
    use_in_migrations = True

    # models = User

    def _create_user(self, email, first_name, last_name, phone, role, username=None, password=None, **extra_fields):
        # def create_user(self, email, first_name, last_name, phone, role, username=None, password=None):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('Users must have an email address')

        # if email:
        #     email = self.normalize_email(email)
        if not username:
            username = email.split("@")[0]
        # if not username:
        #     raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, phone, role, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, first_name=first_name,
                                 last_name=last_name, phone=phone, role=role,
                                 username=username, password=password, **extra_fields)

    # def create_superuser(self, email, password=None, **extra_fields):
    #     """
    #     Create and save a SuperUser with the given email and password.
    #     """
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #     extra_fields.setdefault("is_active", True)
    #
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError(_("Superuser must have is_staff=True."))
    #
    #     return self._create_user(
    #         email=email,
    #         password=password,
    #         **extra_fields
    #     )
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, password=password, **extra_fields)
