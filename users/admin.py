from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
# TODO Aдмика для пользователя - как реализовать ее можно подсмотреть в документаци django
# TODO Обычно её всегда оформляют, но в текущей задачи делать её не обязательно
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'is_verified', 'email', 'phone', 'last_login', 'role', 'image_',)
    readonly_fields = ("image_", )

# admin.site.register(User, UserAdmin)
