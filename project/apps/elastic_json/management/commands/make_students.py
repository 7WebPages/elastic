from django.core.management.base import BaseCommand
import random
import names

from elasticsearch.client import IndicesClient
from elasticsearch import Elasticsearch
from model_mommy import mommy
from elastic_json.models import Student, University, Course
from elastic_json.utils.bulk import put_all_to_index


class Command(BaseCommand):
    help = "generates dummy data for testing/show purposes."

    def add_arguments(self, parser):
        parser.add_argument('count', nargs=1, type=int)

    def handle(self, *args, **options):
        Student.objects.all().delete()
        University.objects.all().delete()
        Course.objects.all().delete()

        # database part
        # make some Universities
        university_names = (
            'MIT', 'MGU', 'CalTech', 'KPI', 'DPI', 'PSTU'
        )
        universities = []
        for name in university_names:
            uni = mommy.make(University, name=name)
            universities.append(uni)
        # make some courses
        template_options = ['CS%s0%s', 'MATH%s0%s', 'CHEM%s0%s', 'PHYS%s0%s']
        courses = []
        for num in range(1, 4):
            for course_num in range(1, 4):
                for template in template_options:
                    name = template % (course_num, num)
                    course = mommy.make(Course, name=name)
                    courses.append(course)
        for _ in xrange(options.get('count')[0]):
            stud = mommy.make(
                Student,
                university=random.choice(universities),
                first_name=names.get_first_name(),
                last_name=names.get_last_name(),
                age=random.randint(17, 25)
            )
            for _ in range(random.randint(1, 4)):
                index = random.randint(0, len(courses)-1)
                stud.courses.add(courses[index])

        # recreate index
        indices_client = IndicesClient(client=Elasticsearch())
        if indices_client.exists('django'):
            indices_client.delete(index='django')
        indices_client.create(index='django')
        indices_client.put_mapping(
            doc_type='student',
            body=Student._meta.es_mapping,
            index='django'
        )
        # update part
        put_all_to_index(Student)
