from django.shortcuts import get_object_or_404
from rest_framework import decorators, permissions, response, status

from api.mixins import ListRetrieveCreateMixins
from api.paginations import CustomPagination
from api.recipes.serializers import (
    SubscribeCreateDeleteSerializer,
    SubscriptionSerializer,
)
from users.models import Subscribe, User
from .serializers import (
    SetPasswordSerializer,
    UserCreteSerializer,
    UserSerializer,
)


class UserViewSet(ListRetrieveCreateMixins):
    """Работа с пользователями"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Выбор сериализатора для обработки данных."""
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreteSerializer

    @decorators.action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        """Получение текущего пользователя."""
        user = request.user
        serializer = UserSerializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def set_password(self, request):
        """Изменение пароля пользователя."""
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        user = request.user
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return response.Response(
            {'detail': 'Пароль успешно изменен.'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @decorators.action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=CustomPagination,
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @decorators.action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            serializer = SubscribeCreateDeleteSerializer(
                author, request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(author=author, user=request.user)

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        subscription = get_object_or_404(
            Subscribe, author=author, user=request.user
        )
        subscription.delete()
        return response.Response(
            {'message': 'Вы успешно отписались'}, status=status.HTTP_200_OK
        )
