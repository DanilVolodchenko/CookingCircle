from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .users.views import UserViewSet
from .recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
