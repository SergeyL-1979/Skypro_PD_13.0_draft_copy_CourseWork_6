from django.contrib.auth.models import (
    BaseUserManager, User
)
from django.urls import reverse


# TODO здесь должен быть менеджер для модели Юзера.
# TODO Поищите эту информацию в рекомендациях к проекту
class UserManager(BaseUserManager):
    models = User

    def create_user(self, email, username, password=None):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(email=self.normalize_email(email), username=username, )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Создает и сохраняет штатного пользователя с указанным адресом электронной почты и паролем.
        """
        user = self.create_user(email, password=password, )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем.
        """

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    # def get_absolute_url(self):
    #     return reverse('edit', kwargs={"pk": self.pk})
