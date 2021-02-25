from django.test import TestCase
from model_bakery import baker
from pprint import pprint


class TestCustomUserModel(TestCase):
    def setUp(self):
        self.custom_user = baker.make('accounts.CustomUser')
        pprint(self.custom_user.__dict__)
