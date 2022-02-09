from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'add_facility', views.add_facility_data, name='add_facility_data'),
    path(r'update_facility/<uuid:facility_id>', views.update_facility_data, name='update_facility_data'),
    path(r'partners', views.partners, name='partners'),
    path(r'sub_counties', views.sub_counties, name='sub_counties'),
    path(r'get_partners_list', views.get_partners_list, name='get_partners_list'),
]