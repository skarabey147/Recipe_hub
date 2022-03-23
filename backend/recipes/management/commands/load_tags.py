import csv

from django.core.management.base import BaseCommand, CommandError

from recipe.models import Tag


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            for csv_file in options['csv_file']:
                datareader = csv.reader(open(csv_file,
                                             encoding='utf-8'),
                                        delimiter=',', quotechar='"')
                for row in datareader:
                    tag = Tag(name=row[0], color=row[1], slug=row[2])
                    tag.save()
        except FileNotFoundError:
            raise CommandError('Добавьте файл tags в директорию data')
