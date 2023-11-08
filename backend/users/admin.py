from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = ('username', 'email')
    list_editable = ('username', 'first_name', 'last_name', 'password')
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    empty_value_display = '---'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    list_editable = ('author',)
    list_select_related = True
    ordering = ('user', 'author')
    empty_value_display = '---'
