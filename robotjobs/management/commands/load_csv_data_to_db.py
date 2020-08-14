from csv import DictReader
from django.core.management import BaseCommand

from robotjobs.models import Testdata, Tag

SUPPORTED_TAG = [
    'Sanity',
    'Intermediate',
    'Full'
]

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the testcase data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from testdata.csv into our base mode"

    def handle(self, *args, **options):
        if Tag.objects.exists() or Testdata.objects.exists():
            print('test case data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Creating testcase data")
        for tag in SUPPORTED_TAG:
            t = Tag(name=tag)
            t.save()
        print("Loading testcase data for tag-Full")
        for row in DictReader(open('./testdata.csv')):
            testdata = Testdata()
            testdata.testsuite = row['Testsuite']
            testdata.testfile = row['Testfile']
            testdata.testcase = row['Testcase']
            testdata.save()
            raw_tag_names = row['Tag']
            tag_names = [name for name in raw_tag_names.split('|') if name]
            for tag_name in tag_names:
                tag_o = Tag.objects.get(name=tag_name)
                testdata.tag.add(tag_o)
            testdata.save()
