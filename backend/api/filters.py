from django_filters.rest_framework import (
    FilterSet,
    ModelMultipleChoiceFilter,
    BooleanFilter,
    NumberFilter,
)

from recipes.models import Recipe, Tag


class RecipeTagFilter(FilterSet):
    """Фильтрация рецептов по тегам
    (их может быть сколько угодно много)."""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = NumberFilter(field_name='author_id')
    is_favorited = BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = BooleanFilter(method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def is_favorited_filter(self, queryset, name, value):
        return queryset.filter(favorite_recipe__user=self.request.user)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return queryset.filter(shopping_recipe__user=self.request.user)
