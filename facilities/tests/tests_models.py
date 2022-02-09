from django.test import TestCase
from ..models import IPdata

class IPdataTestCase(TestCase):
    def setUp(self):
        IPdata.objects.create(city="kisumu", country="kenya", lat="13.654", lon="-2.4256")
        IPdata.objects.create(city="mombasa", country="kenya", lat="3.654", lon="-12.4256")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        kis = IPdata.objects.get(city="kisumu")
        mom = IPdata.objects.get(city="mombasa")
        self.assertEqual(kis.city, 'kisumu')
        self.assertEqual(mom.city, 'mombasa')