from django.contrib import admin
from .models import *

def nullfy_rate(modeladmin, request, queryset):
    queryset.update(rate=0)

nullfy_rate.short_description = 'Обнулить рейтинг'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_author', 'post_type', 'rate', 'creation_time')
    list_filter = ('post_author', 'post_type', 'creation_time')
    search_fields = ('title', 'post_author', 'post_type', 'creation_time')
    actions = [nullfy_rate]

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
