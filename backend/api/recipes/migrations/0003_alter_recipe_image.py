# Generated by Django 3.2 on 2023-07-31 06:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(
                blank=True,
                upload_to='static/recipes/',
                verbose_name='Картинки',
            ),
        ),
    ]