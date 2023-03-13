import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
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


class User(AbstractBaseUser, PermissionsMixin):
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
    # TODO переопределение пользователя.
    # TODO подробности также можно поискать в рекомендациях к проекту
    STATUS = [
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    ]
    username = models.CharField(_('username'), db_index=True, max_length=255)
    email = models.EmailField(_('email'), db_index=True, max_length=60, unique=True, blank=True)
    first_name = models.CharField(_('first_name'), max_length=50)
    last_name = models.CharField(_('last_name'), max_length=50)
    phone = PhoneNumberField(_('phone'), null=False, blank=False)
    last_login = models.DateTimeField(_('last_login'), auto_now=True)
    role = models.CharField(_('role'), max_length=15, choices=STATUS, default='user')
    # role = models.CharField(choices=[(user_role.value, user_role.name) for user_role in UserRoles],
    #                         max_length=15, verbose_name='Роль пользователя')
    image = models.ImageField(_('image'), upload_to="img_users")

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
    is_verified = models.BooleanField(_('Verified'),
                                      default=False,
                                      help_text=_('Обозначает, что у этого пользователя есть все разрешения без их явного назначения.')
                                      )
    # is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    # для корректной работы нам также необходимо
    # переопределить менеджер модели пользователя
    objects = UserManager()

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'
    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        unique_together = ('email', 'phone',)
        # abstract = True

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return f"{self.email}, ({self.get_full_name()})"

    @property
    def is_admin(self):
        # return self.role == UserRoles.ADMIN
        return self.role == 'admin'

    @property
    def is_user(self):
        # return self.role == UserRoles.USER
        return self.role == 'user'

    #
    # @property
    # def is_superuser(self):
    #     return self.is_admin

    @property
    def is_stuff(self):
        return self.role == 'admin'

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
        Returns the first_name plus the last_name, with a space in between.
        """
        # return self.username
        # return self.email
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Аналогично методу get_full_name().
        Returns the short name for the user.
        """
        # return self.username
        # return self.email
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Отправляет электронное письмо пользователю.
        :param subject: ТЕМА СООБЩЕНИЯ
        :param message: ТЕЛО САМОГО СООБЩЕНИЯ
        :param from_email: ОТ КОГО ОТПРАВЛЕНО СООБЩЕНИЕ
        :param kwargs:
        :return:
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + timedelta(days=1)
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token.decode('utf-8')
    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.strftime('%S')
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    # Для проверки разрешений. Для простоты у всех администраторов есть ВСЕ разрешения
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        Возвращает True, если у пользователя есть каждое из указанных разрешений.
        Если объект передан, он проверяет, есть ли у пользователя все необходимые
        разрешения для этого объекта.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
        # return self.is_admin


