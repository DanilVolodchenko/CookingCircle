import csv
import os

from foodgram.settings import BASE_DIR

from ...models import Ingredient

FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


def open_ingredients_file():
    csv_file = open(FILE_PATH, 'r')
    data = csv.reader(csv_file)
    return data


def load_data_to_db():
    data = open_ingredients_file()

    for ingredient_name, measurement_unit in data:
        Ingredient.objects.get_or_create(
            name=ingredient_name,
            measurement_unit=measurement_unit
        )
