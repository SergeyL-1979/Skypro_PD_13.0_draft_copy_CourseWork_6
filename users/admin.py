from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# # Register your models here.
# # TODO Aдминка для пользователя - как реализовать ее можно подсмотреть в документацию django
# # TODO Обычно её всегда оформляют, но в текущей задачи делать её не обязательно
@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('first_name', 'is_verified', 'email', 'phone', 'role', 'image_',)
    readonly_fields = ("image_", "last_login")
    filter_horizontal = ()
    list_filter = ('phone', 'email')
    # add_fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('email', 'first_name', 'last_name',  'image_', 'phone', 'role')}),
    # )
    # # I've added this 'add_fieldset'
    # fieldsets = (
    #     (None, {
    #         "fields": (
    #             ('email', 'first_name', 'last_name', 'image_', 'is_staff', 'phone', 'role')
    #         ),
    #     }),
    # )

# admin.site.register(User, MyUserAdmin)

# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#     model = User
#     list_display = ('phone', 'email')
#     list_filter = ('phone', 'email')
#     search_fields = ('phone',)
#     ordering = ('phone',)
#     filter_horizontal = ()
#     fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('phone',)}),
#                                        )
#     # I've added this 'add_fieldset'
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone', 'password1', 'password2'),
#         }),
#     )
