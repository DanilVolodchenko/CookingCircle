from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import decorators, permissions, response, status, viewsets

from api.filters import RecipeTagFilter
from api.mixins import CreateUpdateDestroyListViewSet
from api.paginations import CustomPagination
from api.permissions import IsOwnerOrReadOnly
from api.utils import get_list_shopping
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeFavoriteSerializer,
    RecipeListSerializer,
    RecipeSubscribeSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тегов )."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(CreateUpdateDestroyListViewSet):
    """Получение, создание, обновление и
    удаление рецептов."""

    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsOwnerOrReadOnly,)
    filterset_class = RecipeTagFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        else:
            return RecipeCreateSerializer

    @decorators.action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        """Добавляет в избранное."""
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            serializer = RecipeFavoriteSerializer(
                recipe, request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(recipe=recipe, user=request.user)

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return response.Response(
            {'detail': 'Рецепт удален из избранного!'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @decorators.action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        """Добавляет в список покупок."""
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = RecipeSubscribeSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        ).delete()
        return response.Response(
            {'detail': 'Рецепт успешно удален из списка покупок.'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @decorators.action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        """Скачивает файл со списком ингредиентов."""
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_recipe__user=request.user
            )
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'total_amount',
                'ingredient__measurement_unit',
            )
        )
        list_shopping = get_list_shopping(ingredients)

        return HttpResponse(
            'Список покупок:\n' + '\n'.join(list_shopping),
            content_type='text/plain',
        )
