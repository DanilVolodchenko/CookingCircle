from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserCreteSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SetPasswordSerializer(serializers.Serializer):
    """Изменение пароля пользователя."""

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        current_password = attrs['current_password']
        if not user.check_password(current_password):
            raise serializers.ValidationError("Текущий пароль не совпадает.")
        return attrs
