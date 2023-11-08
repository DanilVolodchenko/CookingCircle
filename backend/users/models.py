from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Придумайте логин',
    )
    first_name = models.CharField(
        max_length=150, verbose_name='Имя', help_text='Введите ваше имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите вашу фамилию',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribing'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
        )

    def __str__(self):
        return f'{self.user.username} {self.author.username}'
