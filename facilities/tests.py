from django.test import TestCase
from django.urls import reverse

from .models import *


class FacilitiesListViewTest(TestCase):
    def test_homepage_view(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facilities/facilities_list.html')

    def test_sub_counties_lists_all_authors(self):
        # check url is working fine
        response = self.client.get('/facilities/sub_counties')
        self.assertEqual(response.status_code, 200)

    def test_partners_lists_all_authors(self):
        # check url is working fine
        response = self.client.get('/facilities/get_partners_list')
        self.assertEqual(response.status_code, 200)

    def test_agencies_lists_all_authors(self):
        # check url is working fine
        response = self.client.get('/facilities/get_agencies_list')
        self.assertEqual(response.status_code, 200)


class LoginRequiredRedirectsViewTest(TestCase):
    def test_add_facility_redirect(self):
        with self.settings(LOGIN_URL='/user/login/'):
            response = self.client.get('/facilities/add_facility')
            self.assertRedirects(response, '/login/?next=/facilities/add_facility')

    def test_partners_redirect(self):
        with self.settings(LOGIN_URL='/user/login/'):
            response = self.client.get('/facilities/partners')
            self.assertRedirects(response, '/login/?next=/facilities/partners')

    def test_update_facility_redirect(self):
        #self.assertRedirects(response, '/home', status_code=301, target_status_code=301)
        with self.settings(LOGIN_URL='/user/login/'):
            url = '/facilities/update_facility/'+str(uuid.uuid4())
            response = self.client.get(url)
            self.assertRedirects(response, '/login/?next='+url)


class FacilityModelTestCase(TestCase):
    def facility_setup(self):
        facility = Facility_Info.objects.create(id=uuid.uuid4(), mfl_code=41000, name="my_new facility",
                                                county=1, sub_county=1,
                                                lat=2.45, lon=3.67, partner=1, owner=1)
        facility.save()
        self.assertEqual(Facility_Info.objects.count(), 1)

        #self.assertEqual(post.slug, slugify(post.title))
