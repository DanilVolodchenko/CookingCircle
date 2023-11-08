from django.core.management.base import BaseCommand

from .add_ingredients_script import load_data_to_db


class Command(BaseCommand):
    help = 'Добавить ингредиенты в БД'

    def handle(self, *args, **options):
        load_data_to_db()
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно добавлены'))
