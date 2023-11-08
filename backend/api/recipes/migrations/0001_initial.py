# Generated by Django 3.2 on 2023-07-30 16:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=200, verbose_name='Название'),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True,
                        upload_to='recipes/',
                        verbose_name='Картинки',
                    ),
                ),
                ('text', models.TextField(verbose_name='Описание')),
                (
                    'cooking_time',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='Время приготовления (в минутах)',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Дата публикации'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['author'],
            },
        ),
    ]