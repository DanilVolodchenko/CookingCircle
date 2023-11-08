def get_recipes(context, obj, serializer):
    request = context.get('request')
    limit = request.GET.get('recipes_limit')
    recipes = obj.recipes.all()
    if limit:
        recipes = recipes[: int(limit)]
    serializer = serializer(recipes, many=True, read_only=True)
    return serializer.data


def get_recipes_count(obj):
    return obj.recipes.count()


def get_is_subscribe(context, obj, model):
    user = context.get('request').user
    return model.objects.filter(user=user, author=obj).exists()


def get_is_favorited_or_in_shopping(context, obj, model):
    user = context.get('request').user.id
    return model.objects.filter(user=user, recipe=obj).exists()


def get_list_shopping(ingredients):
    list_shopping = []
    for i, ingredient in enumerate(ingredients):
        ingredient_info = f'{i + 1}.' + '{} {}{}'.format(*ingredient)
        list_shopping.append(ingredient_info)

    return list_shopping
