from django.contrib import admin

from ads.models import Ad, Comment


# Register your models here.
# TODO здесь можно подкючить ваши модели к стандартной джанго-админке

class CommentAdAdmin(admin.StackedInline):
    model = Comment
    list_display = ('comment_user',)
    readonly_fields = ('comment_create', 'comment_ad')
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', )


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'price', 'created_at', )
    list_filter = ('created_at', 'author')
    # raw_id_fields = ('author',)
    search_fields = ('title', 'post_text')
    # prepopulated_fields = {'slug': ('headline',), }
    ordering = ['-created_at']
    list_per_page = 10
    list_max_show_all = 100
    # Поле для комментария
    inlines = [CommentAdAdmin, ]


# admin.site.register(Comment)
# admin.site.register(Ad)
