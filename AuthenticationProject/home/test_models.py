from django.test import TestCase
from model_bakery import baker
from pprint import pprint


class TestProjectModel(TestCase):
    def setUp(self):
        self.project = baker.make('home.Project')
        pprint(self.project.__dict__)
