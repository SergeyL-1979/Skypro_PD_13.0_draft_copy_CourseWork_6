from django.db import models

from django.conf import settings

from users.models import User


# Create your models here.
class Ad(models.Model):
    # TODO добавьте поля модели здесь
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=128, name=False, verbose_name='Заголовок')
    price = models.IntegerField()
    image = models.ImageField(upload_to="img_goods", verbose_name='Фото товара')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Comment(models.Model):
    # TODO добавьте поля модели здесь
    """ Модуль хранения комментариев под объявлением """
    comment_ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    comment_text = models.TextField(verbose_name='Текст комментария')
    comment_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')

