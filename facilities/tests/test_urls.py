from django.urls import reverse, resolve
from django.urls import path

class TestUrls:
# here, you are checking if the path's view name is content
    def test_post_content_url(self):
        path = reverse('update_facility_data', kwargs={'facility_id':'f7138a9c-a1d1-4dce-8fcf-d0d3ae655141'})
        assert resolve(path).view_name == "update_facility_data"  # here you are checking if the path's view name is content