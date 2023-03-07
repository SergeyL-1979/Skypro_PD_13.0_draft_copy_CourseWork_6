from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserRoles(models.Model):
    # TODO закончите enum-класс для пользователя
    name_user = models.CharField(max_length=100)
    phone = PhoneNumberField(null=False, blank=False, unique=True)


# class User(AbstractBaseUser):
#     # TODO переопределение пользователя.
#     # TODO подробности также можно поискать в рекоммендациях к проекту
#     pass


# class User(AbstractBaseUser):
#     """
#     Абстрактный базовый класс, реализующий полнофункциональную модель пользователя с правами администратора.
#     Требуется имя пользователя и пароль. Другие поля являются необязательными
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = CIEmailField(_('Email Address'),
#                          unique=True,
#                          error_messages={
#                              'unique': _("Пользователь с таким именем уже существует."),
#                          },
#                          )
#
#     first_name = models.CharField(_('First Name'), max_length=255, blank=True)
#     last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
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
#     date_joined = models.DateTimeField(
#         _('Date Joined'),
#         default=timezone.now
#     )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)