import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'loading ingredients from data in json or csv'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = json.load(f)
                try:
                    objs = [
                        Ingredient(
                            name=ingredient["name"],
                            measurement_unit=ingredient["measurement_unit"])
                        for ingredient in data
                    ]
                    Ingredient.objects.bulk_create(objs)
                except IntegrityError:
                    pass

        except FileNotFoundError:
            raise CommandError('Добавьте файл ingredients в директорию data')
