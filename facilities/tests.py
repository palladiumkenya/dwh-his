from django.test import TestCase
from django.urls import reverse


class FacilitiesListViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facilities/facilities_list.html')

    def test_sub_counties_lists_all_authors(self):
        # check url is working fine
        response = self.client.get('/facilities/sub_counties')
        self.assertEqual(response.status_code, 200)


class LoginRequiredRedirectsViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/facilities/add_facility')
        self.assertRedirects(response, '/user/login')
