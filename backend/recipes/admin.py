from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'image', 'text', 'cooking_time')
    list_filter = ('author', 'name', 'cooking_time')
    list_editable = ('name', 'image', 'text', 'cooking_time')
    search_fields = ('author', 'name', 'pub_date')
    ordering = ('author', 'pub_date')
    list_select_related = True
    empty_value_display = '---'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    list_editable = ('recipe',)
    search_fields = (
        'user',
        'recipe',
    )
    ordering = ('user',)
    list_select_related = True
    empty_value_display = '---'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient', 'amount')
    list_editable = ('amount',)
    search_fields = ('recipe', 'ingredient')
    ordering = (
        'recipe',
        'amount',
    )
    list_select_related = True
    empty_value_display = '---'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('user',)
    list_select_related = True
    empty_value_display = '---'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color')
    list_editable = ('color', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)
    empty_value_display = '---'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('^name',)
    ordering = ('name',)
    empty_value_display = '---'
