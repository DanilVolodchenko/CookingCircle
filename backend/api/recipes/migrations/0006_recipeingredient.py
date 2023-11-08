# Generated by Django 3.2 on 2023-08-02 07:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0005_auto_20230802_0124'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
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
                    'amount',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='Количество',
                    ),
                ),
                (
                    'ingredient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ingredient',
                        to='ingredients.ingredient',
                        verbose_name='Ингредиент',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipes',
                        to='recipes.recipe',
                        verbose_name='Рецепт',
                    ),
                ),
            ],
        ),
    ]
