from django.core.management.base import BaseCommand
from elastic_json.models import Student
from elastic_json.utils.bulk import put_all_to_index


class Command(BaseCommand):
    help = "generates elasticsearch indexes described in models."

    def handle(self, *args, **options):
        put_all_to_index(Student)
