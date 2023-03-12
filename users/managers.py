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

        if extra_fields.get('is_superuser'):
            user = self.model(
                username=username,
                **extra_fields
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

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )

    # def create_superuser(self, email, first_name, last_name, phone, role='admin', password=None):
    #     """
    #     Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем.
    #     Функция для создания суперпользователя — с ее помощью мы создаем администратора
    #     это можно сделать с помощью команды createsuperuser
    #     """
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         first_name=first_name,
    #         last_name=last_name,
    #         phone=phone,
    #         password=password,
    #         # role="admin",
    #         role=role
    #     )
    #
    #     # user.is_admin = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user

    # def get_absolute_url(self):
    #     return reverse('edit', kwargs={"pk": self.pk})

# class UserManager(BaseUserManager):
#
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given email and password.
#         """
#         if not email:
#             raise ValueError(_("The Email must be set"))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError(_("Superuser must have is_staff=True."))
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError(_("Superuser must have is_superuser=True."))
#         return self.create_user(email, password, **extra_fields)
