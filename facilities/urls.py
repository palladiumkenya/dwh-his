from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path(r'facilities/add_facility', views.add_facility_data, name='add_facility_data'),
    path(r'facilities/update_facility/<uuid:facility_id>', views.update_facility_data, name='update_facility_data'),
    path(r'facilities/approve_changes/<uuid:facility_id>', views.approve_facility_changes, name='approve_facility_changes'),
    path(r'facilities/delete_facility/<uuid:facility_id>', views.delete_facility, name='delete_facility'),
    path(r'facilities/partners', views.partners, name='partners'),
    path(r'facilities/sub_counties', views.sub_counties, name='sub_counties'),
    path(r'facilities/add_sub_counties', views.add_sub_counties, name='add_sub_counties'),
    path(r'facilities/get_partners_list', views.get_partners_list, name='get_partners_list'),
    path(r'facilities/get_agencies_list', views.get_agencies_list, name='get_agencies_list'),
    # path(r'fill_database', views.fill_database, name='fill_database'),
    path(r'test_email', views.test_email, name='test_email'),
    path(r'send_customized_email', views.send_customized_email, name='send_customized_email'),
    # path(r'add_stewards', views.add_stewards, name='add_stewards'),
    path(r'combineexcelandapi', views.combineexcelandapi, name='combineexcelandapi'),
path(r'searchmflcodeinapi', views.searchmflcodeinapi, name='searchmflcodeinapi'),
path(r'addsubcountiesinapi', views.addsubcountiesinapi, name='addsubcountiesinapi'),
path(r'addpartnersinexcel', views.addpartnersinexcel, name='addpartnersinexcel'),
path(r'addownersinapi', views.addownersinapi, name='addownersinapi'),
]