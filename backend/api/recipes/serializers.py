from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.users.serializers import UserSerializer
from api.utils import (
    get_recipes,
    get_is_favorited_or_in_shopping,
    get_is_subscribe,
    get_recipes_count,
)
from users.models import Subscribe, User
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Создание ингредиента для рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeIngredientListSerializer(serializers.ModelSerializer):
    """Получение ингредиента рецепта."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Получение рецепта."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientListSerializer(
        read_only=True, many=True, source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Подписан ли пользователь на рецепт."""
        return get_is_favorited_or_in_shopping(self.context, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        """Находиться ли рецепт в списке рецептов."""
        return get_is_favorited_or_in_shopping(self.context, obj, ShoppingCart)


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта."""

    author = UserSerializer(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        """Сохрание рецепта в БД."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        """Обновление данных в БД."""
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            for ingredient in ingredients:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    """Добавляет в список покупок."""

    name = serializers.ReadOnlyField()
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Добавление рецептов в избранное."""

    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ['name', 'cooking_time']

    def validate(self, attrs):
        recipe = self.instance
        user = self.context['request'].user
        if Favorite.objects.filter(recipe=recipe, user=user):
            raise serializers.ValidationError('Вы подписаны на этот рецепт')
        return attrs


class SubscriptionSerializer(serializers.ModelSerializer):
    """Подписка на автора рецепта."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        """Подписан ли на автора рецепта."""
        return get_is_subscribe(self.context, obj, Subscribe)

    def get_recipes(self, obj):
        """Получение рецептов."""
        return get_recipes(self.context, obj, RecipeSubscribeSerializer)

    def get_recipes_count(self, obj):
        """Получение количества рецептов."""
        return get_recipes_count(obj)


class SubscribeCreateDeleteSerializer(serializers.ModelSerializer):
    """Создания и удаления подписки."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSubscribeSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]
        read_only_fields = ['email', 'username', 'first_name', 'last_name']

    def get_is_subscribed(self, obj):
        """Подписан ли на автора рецепта."""
        return get_is_subscribe(self.context, obj, Subscribe)

    def get_recipes(self, obj):
        """Получение рецептов."""
        return get_recipes(self.context, obj, RecipeSubscribeSerializer)

    def get_recipes_count(self, obj):
        """Получение количества рецептов."""
        return get_recipes_count(obj)

    def validate(self, attrs):
        user = self.context['request'].user
        author = self.instance
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора!'
            )
        return attrs
