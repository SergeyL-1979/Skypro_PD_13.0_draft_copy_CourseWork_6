from datetime import datetime
from enum import Enum

import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Create your models here.
# class UserRoles(Enum):
#     """ ENUM-class для перечисления вариантов """
#     # закончите enum-класс для пользователя
#     USER = 'Пользователь'
#     ADMIN = 'Администратор'


class User(AbstractBaseUser):
    """
    Создание модели пользователя.
    Необходимые поля:
    - first_name — имя пользователя (строка).
    - last_name — фамилия пользователя (строка).
    - phone — телефон для связи (строка).
    - email — электронная почта пользователя (email) **(используется в качестве логина).**
    - role — роль пользователя, доступные значения: user, admin.
    - image - аватарка пользователя
    """
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    # TODO переопределение пользователя.
    # TODO подробности также можно поискать в рекомендациях к проекту
    STATUS = [
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    ]
    # usename = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, max_length=60, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Телефон')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний визит')
    role = models.CharField(max_length=5, choices=STATUS, default='user')
    # role = models.CharField(choices=[(user_role.value, user_role.name) for user_role in UserRoles],
    #                         max_length=15, verbose_name='Роль пользователя')
    image = models.ImageField(upload_to="img_users", verbose_name='Аватарка пользователя')
    # is_active = models.BooleanField(default=True)

    def image_(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
    image_.short_description = 'Аватарка пользователя'
    image_.allow_tags = True

    is_active = models.BooleanField(_('Active'),
                                    default=True,
                                    help_text=_(
                                        'Указывает, следует ли считать этого пользователя активным. '
                                        'Отменить выбор вместо удаления учетных записей'
                                    ),
                                    )

    is_staff = models.BooleanField(_('Staff Status'),
                                   default=False,
                                   help_text=_('Определяет, может ли пользователь войти на этот сайт администратора.'),
                                   )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """ Позволяет получить токен пользователя путем вызова user.token, вместо
        user.__generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        # return self.username
        return self.email

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        # return self.username
        return self.email

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')



# =====================================================================================================
# class User(AbstractBaseUser):
#     """
#     Абстрактный базовый класс, реализующий полнофункциональную модель пользователя с правами администратора.
#     Требуется имя пользователя и пароль. Другие поля являются необязательными
#     """
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     # email = CIEmailField(_('Email Address'), unique=True, error_messages={
#     #                          'unique': _("Пользователь с таким именем уже существует."),
#     #                      },
#     #                      )
#     email = models.EmailField()
#
#     first_name = models.CharField(_('First Name'), max_length=255, blank=True)
#     last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
#
#     last_login = models.DateTimeField(auto_now=True)
#     phone = PhoneNumberField(null=False, blank=False, unique=True)
#     role = models.CharField(max_length=10)
#
#     is_staff = models.BooleanField(_('Staff Status'),
#                                    default=False,
#                                    help_text=_('Определяет, может ли пользователь войти на этот сайт администратора.'),
#                                    )
#
#     is_active = models.BooleanField(_('Active'),
#                                     default=True,
#                                     help_text=_(
#                                         'Указывает, следует ли считать этого пользователя активным. '
#                                         'Отменить выбор вместо удаления учетных записей'
#                                     ),
#                                     )
#
#     # Audit Values
#     is_email_confirmed = models.BooleanField(
#         _('Email Confirmed'),
#         default=False
#     )
#     date_joined = models.DateTimeField(_('Date Joined'), default=datetime.now)
#
#     objects = UserManager()
#
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [
#         'first_name',
#         'last_name'
#     ]
#
#     class Meta:
#         verbose_name = _('User')
#         verbose_name_plural = _('Users')
#
#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)
#
#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         return f"{self.first_name} {self.last_name}"
#
#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Отправить электронное письмо этому пользователю."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)
