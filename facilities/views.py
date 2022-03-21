from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import uuid
import mysql.connector
from django.contrib.auth.decorators import login_required
# import xlsxwriter

from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import pandas as pd
import excel2json
from django.contrib.auth.models import User

import os
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings

from .models import *
from .forms.facilities.forms import *

from requests.structures import CaseInsensitiveDict
import requests
import json


def test_email(request):
    demain = request.META['HTTP_HOST']
    print("domain", demain, request.scheme)
    print(request.scheme + request.META[
        'HTTP_HOST'] + '/facilities/update_facility/' + '981893d7-8488-4319-b976-747873551b71')
    context = {
        'news': 'We have good news!',
        'url': request.scheme + "://" + request.META['HTTP_HOST'] + '/facilities/update_facility/',
        'mfl_code': 122345,  # facilitydata.mfl_code,
        'facility_id': '981893d7-8488-4319-b976-747873551b71',  # facilitydata.id
        'username': 123456
    }
    msg_html = render_to_string('facilities/email_template.html', context)
    msg = EmailMessage(subject="Facility Modified", body=msg_html, from_email=settings.DEFAULT_FROM_EMAIL,
                       bcc=['marykilewe@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    print('-----------> sending mail ...')
    return 0


def send_email(scheme, domain, user_names, facility_id, mfl_code, partner_id):
    context = {
        'news': 'We have good news!',
        'url': scheme + "://" + domain + '/facilities/update_facility/',
        'mfl_code': mfl_code,  # facilitydata.mfl_code,
        'facility_id': facility_id,  # facilitydata.id
        'username': user_names
    }
    organization = Organization_stewards.objects.get(organization=partner_id)

    msg_html = render_to_string('facilities/email_template.html', context)
    msg = EmailMessage(subject="Facility Modified", body=msg_html, from_email=settings.DEFAULT_FROM_EMAIL,
                       bcc=['marykilewe@gmail.com'])  # , organization.email
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    print('-----------> sending mail ...', organization.email)
    return 0


@csrf_exempt
def send_customized_email(request):
    if request.method == 'GET':
        facility_id = request.GET['facility_id']
        choice = request.GET['choice']
        reason = request.GET['reason']
        print("--------", facility_id)

        facilitydata = Facility_Info.objects.prefetch_related('partner') \
            .select_related('owner').select_related('county') \
            .select_related('sub_county').get(pk=facility_id)

        if choice == "approved":
            message_title = "Approved!"
            message = "Changes you made now reflect on the portal!"
            subject = "Facility Changes Approved!"
        else:
            message_title = "Rejected!"
            message = "Reasons provided for the rejection are : "
            subject = "Facility Changes Rejected!"

        edits = Edited_Facility_Info.objects.get(facility_info=facility_id)
        # user = User.objects.get(pk=edits.user_edited)
        print("the user is", edits.user_edited_name, edits.user_edited_email)

        context = {
            'news': 'We have good news!',
            'url': request.scheme + "://" + request.META['HTTP_HOST'] + '/facilities/update_facility/',
            'mfl_code': facilitydata.mfl_code,
            'facility_id': facilitydata.id,
            "message_title": message_title,
            "reason_given": reason,
            "choice": choice,
            "message": message,
            "user_name": edits.user_edited_name
        }
        msg_html = render_to_string('facilities/customizable_email.html', context)
        msg = EmailMessage(subject=subject, body=msg_html, from_email=settings.DEFAULT_FROM_EMAIL,
                           bcc=[edits.user_edited_email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print('-----------> sending customized mail ...', choice)
    return HttpResponse(0)


def fetch_sdp_and_agencies(request):
    file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/HIS Implementation List .xlsx")
    # make json sheet of excel file
    excel_data_df = pd.read_excel(file, sheet_name='Facilities')
    # json_str = excel_data_df.to_json()
    main_sdps = []
    for num in range(0,13720):
        facilityObj = {}
        facilityObj['Facilitycode'] = int(excel_data_df['Facilitycode'][num])
        facilityObj['SDP'] = excel_data_df['Implementing_Mechanism_Name'][num] if str(excel_data_df['Implementing_Mechanism_Name'][num]) != "nan" \
                            else ""

        main_sdps.append(facilityObj)
    # print(main_sdps)
    # print('Excel Sheet to JSON:\n', json_str)
    jsondata = json.dumps(main_sdps)
    f = open("sdps_and_agencies.json", "w+")
    f.write(jsondata)
    f.close()
    return 0


def fecth_mfl_codes(request):
    # fetch data from excel sheet saved as json
    f = open(os.path.join(Path(__file__).resolve().parent.parent, "sdps_and_agencies.json"), 'r')
    excel_facilities = json.load(f)

    # fetch data from kmhfl api
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer ruIuuCIRT5VLvY2cwuvICe6uoNKJ2q"
    url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json'
    response = requests.get(url, headers=headers)

    data = json.loads(response.content)

    # for i in range(0, len(data['results'])):
    #     # loop through facilities in file and search page for it
    #     for fac in excel_facilities:
    #         # print(next(iter(fac.keys())))
    #         if fac["Facilitycode"] == data['results'][i]['code']:
    #             print("Found page 1--->", data['results'][i]['code'], "-----> index :", i)
    #             SDP = Partners.objects.get(name=fac["SDP"]) if fac["SDP"] != "" else None
    #             lat_long = data['results'][i]["lat_long"] if data['results'][i]["lat_long"] else [None, None]
    #
    #             Master_Facility_List.objects.get_or_create(current_page=data['current_page'],
    #                                                current_index=i,
    #                                        mfl_code= data['results'][i]['code'],
    #                                             name=data['results'][i]['name'],
    #                                  county=Counties.objects.get(name=data['results'][i]['county_name']),
    #                                  sub_county=Sub_counties.objects.get(
    #                                      name=data['results'][i]['sub_county_name']),
    #                                  owner=Owner.objects.get(name=data['results'][i]['owner_type_name']),
    #                                  partner=SDP,
    #                                  lat=lat_long[0],
    #                                  lon=lat_long[1])

    for i in range(2, 420):  # data['total_pages']
        # print("Page on ", i)
        next_url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json&page=' + str(i)
        next_page_response = requests.get(next_url, headers=headers)

        next_page_data = json.loads(next_page_response.content)

        for i in range(0, len(next_page_data['results'])):
            # loop through facilities in file and search page for it
            for fac in excel_facilities:
                # print(next(iter(fac.keys())))
                if fac['Facilitycode'] == next_page_data['results'][i]['code']:
                    # print("Found --->", next_page_data['results'][i]['code'], "-----> Page :", i)

                    try:
                        #add any missing sub counties
                        Sub_counties.objects.get_or_create(name=next_page_data['results'][i]['sub_county_name'],
                                                           county=Counties.objects.get(name=next_page_data['results'][i]['county_name']))

                        SDP = Partners.objects.get(name=fac["SDP"]) if fac["SDP"] != "" else None
                        lat_long = next_page_data['results'][i]["lat_long"] if next_page_data['results'][i]["lat_long"] else [None, None]
                        sub_county = Sub_counties.objects.get(name=next_page_data['results'][i]['sub_county_name']) \
                                    if next_page_data['results'][i]['sub_county_name'] else None
                        county = Counties.objects.get(name=next_page_data['results'][i]['county_name'])  \
                                    if next_page_data['results'][i]['county_name'] else None

                        Master_Facility_List.objects.get_or_create(current_page=next_page_data['current_page'],
                                                                       current_index=i,
                                                               mfl_code= next_page_data['results'][i]['code'],
                                                                    name=next_page_data['results'][i]['name'],
                                                         county=county, sub_county=sub_county,
                                                         owner=Owner.objects.get(name=next_page_data['results'][i]['owner_type_name']),
                                                         partner=SDP,
                                                         lat=lat_long[0],
                                                         lon=lat_long[1]
                        )
                    except Exception as e:
                        print('Exception ---------->', e, fac["SDP"], next_page_data['results'][i]['sub_county_name'], next_page_data['results'][i]['county_name'])

    return 0

def add_stewards(request):
    # file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/kenyahmis_stewards.xlsx")
    # stewards_data = pd.read_excel(file)  # reading file
    # make json sheet of excel file
    # excel_data_df = pd.read_excel(file, sheet_name='Sheet2')
    # json_str = excel_data_df.to_json()
    # print('Excel Sheet to JSON:\n', json_str)
    # f = open("stewards.json", "w+")
    # f.write(json_str)
    # f.close()

    f = open(os.path.join(Path(__file__).resolve().parent.parent, "facilities/stewards.json"), 'r')
    data = json.load(f)
    print(len(data))

    main_keys = []
    for dic in data:
        main_keys.append(dic)
        print(len(data[dic]))

    for num in range(0, len(data["Number"])):
        stewardObj = []
        for key in main_keys:
            stewardObj.append(data[key][str(num)])
        print(stewardObj)
        # Partners.objects.create(name=stewardObj[2]).save()
        Organization_stewards.objects.create(steward=stewardObj[1],
                                             organization=Partners.objects.get(name=stewardObj[2]),
                                             email=stewardObj[3],
                                             tel_no=stewardObj[4],
                                             ).save()

    return 0


def combineexcelandapi(request):
    file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/HIS Implementation List .xlsx")
    facilities = pd.read_excel(file, sheet_name='Fridah')  # reading file

    facilities_list = []
    for i in range(0, 30):
        facilityObj = {}
        facilityObj[str(facilities['MFL_Code'][i])] = {"name": facilities['Facility Name'][i],
                                                       "county": facilities['County'][i],
                                                       "sub_County": facilities['SubCounty'][i],
                                                       "owner": facilities['Owner'][i],
                                                       "lat": facilities['Latitude'][i],
                                                       "lon": facilities['Longitude'][i],
                                                       "partner": facilities['SDP'][i],
                                                       "sdp_agency": facilities['SDP Agency'][i],
                                                       "implementation": str(facilities['Implementation'][i]),
                                                       "emr": str(facilities['EMR'][i]),
                                                       "emr_status": str(facilities['EMR Status'][i]),
                                                       "hts_use": str(facilities['HTS Use'][i]),
                                                       "hts_deployment": str(facilities['HTS Deployment'][i]),
                                                       "hts_status": str(facilities['HTS Status'][i]),
                                                       "il_status": str(facilities['IL Status'][i]),
                                                       "webADT_registration": str(facilities['Registration IE'][i]),
                                                       "webADT_pharmacy": str(facilities['Phamarmacy IE'][i]),
                                                       "mlab": str(facilities['mlab'][i]),
                                                       "Ushauri": str(facilities['Ushauri'][i]),
                                                       "Nishauri": str(facilities['Nishauri'][i]),
                                                       "OVC": str(facilities['OVC'][i]),
                                                       "OTZ": str(facilities['OTZ'][i]),
                                                       "PrEP": str(facilities['PrEP'][i]),
                                                       "3PM": str(facilities['3PM'][i]),
                                                       "AIR": str(facilities['AIR'][i]),
                                                       "KP": str(facilities['KP'][i]),
                                                       "MCH": str(facilities['MCH'][i]),
                                                       "TB": str(facilities['TB'][i]),
                                                       "Lab Manifest": str(facilities['Lab Manifest'][i]),
                                                       }
        facilities_list.append(facilityObj)

    print(facilities_list)

    jsonString = json.dumps(facilities_list)
    jsonFile = open("facilites_from_excel.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    return 0


def addpartnersinexcel(request):
    file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/HIS Implementation List .xlsx")
    # make json sheet of excel file
    excel_facilities = pd.read_excel(file, sheet_name='Master_HIS_List')

    for i in range(0, 1732):  # data['total_pages']:
        try:
            emr = excel_facilities['HTS Use'][i]
            if emr != None or emr != "":
                # agency = (excel_facilities['Agency'][i]).strip() if str(excel_facilities['Agency'][i]) != 'nan' else None
                # if agency != None:
                #     SDP_agencies.objects.get_or_create(name=agency)
                HTS_use_type.objects.get_or_create(hts_use_name=emr.strip())
        except Exception as e:
            print('owners with problems ------------->', excel_facilities['County'][i])
            print(e)

    return 0


def addownersinapi(request):
    # fetch data from kmhfl api
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer Co5oG8q1RJMnjuXrqunEyPg6iV5s3M"
    url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json'
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    # Owner.objects.get_or_create(name=(data['results'][i]['owner_type_name']).strip())

    for i in range(2, 420):  # data['total_pages']
        next_url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json&page=' + str(i)
        next_page_response = requests.get(next_url, headers=headers)

        next_page_data = json.loads(next_page_response.content)

        for i in range(0, len(next_page_data['results'])):
            try:
                Owner.objects.get_or_create(name=(next_page_data['results'][i]['owner_type_name']).strip())
                print(next_page_data['results'][i]['owner_type_name'])
            except Exception as e:
                print(e)

    return 0


def addsubcountiesinapi(request):
    # fetch data from kmhfl api
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer Co5oG8q1RJMnjuXrqunEyPg6iV5s3M"

    for i in range(2, 420):  # data['total_pages']
        url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json&page=' + str(i)
        response = requests.get(url, headers=headers)

        data = json.loads(response.content)

        for i in range(0, len(data['results'])):
            try:
                Sub_counties.objects.get_or_create(name=(data['results'][i]['sub_county_name']).strip(),
                                                   county=Counties.objects.get(name=data['results'][i]['county_name']))
            except Exception as e:
                print(data['results'][i]['county_name'])

    return 0


def searchmflcodeinapi(request):
    file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/HIS Implementation List .xlsx")
    # make json sheet of excel file
    excel_facilities = pd.read_excel(file, sheet_name='Master_HIS_List')

    for i in range(0, 30):  # data['total_pages']:

        unique_facility_id = uuid.uuid4()

        Facility_Info(id=unique_facility_id, mfl_code=excel_facilities['MFL_Code'][i],
                                     name=excel_facilities['Facility Name'][i],
                                     county=Counties.objects.get(name=excel_facilities['County'][i]),
                                     sub_county=Sub_counties.objects.get(
                                         name=excel_facilities['SubCounty'][i]),
                                     owner=Owner.objects.get(name=excel_facilities['Owner'][i]),
                                     partner=Partners.objects.get(name=excel_facilities['SDP'][i]),
                                     lat=excel_facilities['Latitude'][i],
                                     lon=excel_facilities['Longitude'][i],
                                     kmhfltest_id=None
                                     ).save()

        # save Implementation info

        CT = True if 'CT' in excel_facilities['Implementation'][i] else False
        HTS = True if 'HTS' in excel_facilities['Implementation'][i] else False
        IL = True if 'IL' in excel_facilities['Implementation'][i] else False
        Implementation_type(ct=CT, hts=HTS, il=IL,
                            for_version="original",
                            facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

        # save HTS info
        if HTS:
            if excel_facilities['HTS Deployment'][i] != 'Desktop':
                deployment = HTS_deployment_type.objects.get(deployment="Desktop Only")
            elif  excel_facilities['HTS Deployment'][i] != 'Mobile & Desktop':
                deployment = HTS_deployment_type.objects.get(deployment="Hybrid")
            else:
                deployment = HTS_deployment_type.objects.get(deployment=excel_facilities['HTS Deployment'][i])


            try:
                use = HTS_use_type.objects.get(hts_use_name=excel_facilities['HTS Use'][i])
            except HTS_use_type.DoesNotExist:
                use = None
            HTS_Info(hts_use_name=use,
                     status=excel_facilities['HTS Status'][i],
                     deployment=deployment,
                     for_version="original",
                     facility_info=Facility_Info.objects.get(pk=unique_facility_id),
                     facility_edits=None).save()
        else:
            # save HTS info
            HTS_Info(hts_use_name=None, status=None, deployment=None,
                     for_version="original",
                     facility_info=Facility_Info.objects.get(pk=unique_facility_id),
                     facility_edits=None).save()

        # save EMR info
        if CT:
            try:
                emr = EMR_type.objects.get(type=excel_facilities['EMR'][i])
            except EMR_type.DoesNotExist:
                emr = None

            EMR_Info(type=emr, status=excel_facilities['EMR Status'][i],
                     ovc=change_value(excel_facilities['OVC'][i]), otz=change_value(excel_facilities['OTZ'][i]),
                     prep=change_value(excel_facilities['PrEP'][i]),
                     tb=change_value(excel_facilities['TB'][i]), kp=change_value(excel_facilities['KP'][i]),
                     mnch=change_value(excel_facilities['MCH'][i]),
                     lab_manifest=change_value(excel_facilities['Lab Manifest'][i]),
                     for_version="original", facility_edits=None,
                     facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
        else:
            EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
                     tb=None, kp=None, mnch=None, lab_manifest=None,
                     for_version="original", facility_edits=None,
                     facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

        # save IL info
        if IL:
            IL_Info(webADT_registration=change_value(excel_facilities['Registration IE'][i]),
                    webADT_pharmacy=change_value(excel_facilities['Phamarmacy IE'][i]),
                    status=excel_facilities['IL Status'][i], three_PM=change_value(excel_facilities['3PM'][i]),
                    for_version="original", facility_edits=None,
                    facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
        else:
            IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                    for_version="original", facility_edits=None,
                    facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

        # save MHealth info
        MHealth_Info(Ushauri=change_value(excel_facilities['Ushauri'][i]), C4C=None,
                     Nishauri=change_value(excel_facilities['Nishauri'][i]), ART_Directory=None,
                     Psurvey=None, Mlab=change_value(excel_facilities['mlab'][i]),
                     for_version="original", facility_edits=None,
                     facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()


    return 0


def change_value(value):
    if value == "Yes":
        return True
    elif value == "No":
        return False
    else:
        return None

def ignore_unkowns(item):
    list_of_unkowns = ['', 'NULL', 'N/A', 'No EMR', 'No HTS Use', 'Yes']
    if item in list_of_unkowns:
        emr = None
        list_of_unkowns.append(item)
        emr = item
    else:
        emr = item
    return emr



def index(request):
    if 'logged_in_user_org' in request.session:
        organization = Organizations.objects.select_related('org_access_right').get(organization_id=request.session["logged_in_user_org"])
        print('logged_in_user_org ---------->', organization.access_right)
        if organization.org_access_right:
            facilities_info = Facility_Info.objects.select_related('partner') \
                .select_related('county') \
                .select_related('sub_county').filter(partner__id=organization.org_access_right.id)
        else:
            facilities_info = Facility_Info.objects.prefetch_related('partner') \
                .select_related('county') \
                .select_related('sub_county').all()
    else:
        facilities_info = Facility_Info.objects.prefetch_related('partner') \
            .select_related('county') \
            .select_related('sub_county').all()

    facilitiesdata = []
    try:
        for row in facilities_info:
            implementation_info = Implementation_type.objects.get(facility_info=row.id)
            emr_info = EMR_Info.objects.get(facility_info=row.id)
            hts_info = HTS_Info.objects.get(facility_info=row.id)
            il_info = IL_Info.objects.get(facility_info=row.id)
            mhealth_info = MHealth_Info.objects.get(facility_info=row.id)

            ct = "CT" if implementation_info.ct else ""
            hts = "HTS" if implementation_info.hts else ""
            il = "IL" if implementation_info.il else ""

            implementation = [ct, hts, il]

            dataObj = {}
            dataObj["id"] = row.id
            dataObj["mfl_code"] = row.mfl_code
            dataObj["name"] = row.name
            dataObj["county"] = row.county
            dataObj["sub_county"] = row.sub_county
            dataObj["owner"] = row.owner.name if row.owner else ""
            dataObj["lat"] = row.lat if row.lat else ""
            dataObj["lon"] = row.lon if row.lon else ""
            dataObj["partner"] = row.partner.name if row.partner else ""
            dataObj["agency"] = row.partner.agency.name if row.partner and row.partner.agency else ""
            dataObj["implementation"] = implementation
            dataObj["emr_type"] = emr_info.type.type if emr_info.type else ""
            dataObj["emr_status"] = emr_info.status if emr_info.status else ""
            dataObj["hts_use"] = hts_info.hts_use_name.hts_use_name if hts_info.hts_use_name else ""
            dataObj["hts_deployment"] = hts_info.deployment.deployment if hts_info.deployment else ""
            dataObj["hts_status"] = hts_info.status
            dataObj["il_status"] = il_info.status
            dataObj["il_registration_ie"] = il_info.webADT_registration
            dataObj["il_pharmacy_ie"] = il_info.webADT_pharmacy
            dataObj["mhealth_ovc"] = mhealth_info.Nishauri

            facilitiesdata.append(dataObj)
    except Exception as e:
        print('ERROR --------->', e)
        # messages.add_message(request, messages.ERROR,
        #                      'A problem was encountered when fetching facility data. Please try again.')
        # return HttpResponseRedirect('/home')

    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None

    return render(request, 'facilities/facilities_list.html', {'facilitiesdata': facilitiesdata,
                                                               'loggedin_user': loggedin_user})


# @login_required(login_url='/login/')
def add_sub_counties(request):
    if request.method == 'POST':
        form = Sub_Counties_Form(request.POST)
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))

        if form.is_valid():
            subcounty = Sub_counties(name=(form.cleaned_data['add_sub_county']).strip(),
                                     county=Counties.objects.get(pk=int(form.cleaned_data['county']))).save()
            messages.add_message(request, messages.SUCCESS,
                                 'Sub county was successfully added and can be viewed below!')
            return HttpResponseRedirect('/facilities/add_sub_counties')
    else:
        form = Sub_Counties_Form()
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))

    return render(request, 'facilities/add_sub_counties.html', {'form': form, "title": "Add sub_counties"})


# @login_required(login_url='/login/')
def add_facility_data(request):
    if 'logged_in_username' not in request.session:
        return HttpResponseRedirect("/signup")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

        if form.is_valid():
            try:
                unique_facility_id = uuid.uuid4()
                # Save the new category to the database.
                facility = Facility_Info.objects.create(id=unique_facility_id, mfl_code=form.cleaned_data['mfl_code'],
                                                        name=form.cleaned_data['name'],
                                                        county=Counties.objects.get(
                                                            pk=int(form.cleaned_data['county'])),
                                                        sub_county=Sub_counties.objects.get(
                                                            pk=int(form.cleaned_data['sub_county'])),
                                                        owner=Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                                                        partner=Partners.objects.get(
                                                            pk=int(form.cleaned_data['partner'])) if form.cleaned_data[
                                                                                                         'partner'] != "" else None,
                                                        # facilitydata.agency = facilitydata.partner.agency.name
                                                        lat=form.cleaned_data['lat'],
                                                        lon=form.cleaned_data['lon']
                                                        )

                facility.save()

                # save Implementation info
                implementation_info = Implementation_type(ct=form.cleaned_data['CT'],
                                                          hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                          for_version="original",
                                                          facility_info=Facility_Info.objects.get(
                                                              pk=unique_facility_id))

                implementation_info.save()

                if form.cleaned_data['HTS'] == True:
                    # save HTS info
                    hts_info = HTS_Info(hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                        status=form.cleaned_data['hts_status'],
                                        deployment=HTS_deployment_type.objects.get(
                                            pk=int(form.cleaned_data['hts_deployment'])),
                                        for_version="original",
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    hts_info.save()
                else:
                    # save HTS info
                    hts_info = HTS_Info(hts_use_name=None, status=None, deployment=None,
                                        for_version="original",
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    hts_info.save()

                # save EMR info
                if form.cleaned_data['CT'] == True:
                    emr_info = EMR_Info(type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                                        status=form.cleaned_data['emr_status'],
                                        ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                                        prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                                        kp=form.cleaned_data['kp_offered'], mnch=form.cleaned_data['mnch_offered'],
                                        lab_manifest=form.cleaned_data['lab_man_offered'],
                                        for_version="original",
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    emr_info.save()
                else:
                    emr_info = EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
                                        tb=None, kp=None, mnch=None, lab_manifest=None,
                                        for_version="original",
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    emr_info.save()

                # save IL info
                if form.cleaned_data['IL'] == True:
                    il_info = IL_Info(webADT_registration=form.cleaned_data['webADT_registration'],
                                      webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                      status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['il_three_PM'],
                                      air=form.cleaned_data['il_air'], Ushauri=form.cleaned_data['il_ushauri'],
                                      Mlab=form.cleaned_data['il_mlab'],
                                      for_version="original",
                                      facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    il_info.save()
                else:
                    il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                                      air=None, Ushauri=None, Mlab=None,
                                      for_version="original",
                                      facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    il_info.save()

                # save MHealth info
                mhealth_info = MHealth_Info(Ushauri=form.cleaned_data['mhealth_ushauri'], C4C=form.cleaned_data['mhealth_c4c'],
                                            Nishauri=form.cleaned_data['mhealth_nishauri'],
                                            ART_Directory=form.cleaned_data['mhealth_art'],
                                            Psurvey=form.cleaned_data['mhealth_psurvey'], Mlab=form.cleaned_data['mhealth_mlab'],
                                            for_version="original",
                                            facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                mhealth_info.save()

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS,
                                     'Facility was successfully added and can be viewed below!')
                return HttpResponseRedirect('/home')
            except Exception as e:
                print("ERROR --------> ", e)
                messages.add_message(request, messages.ERROR,
                                     'A problem was encountered when submitting facility data. Please try again.')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Facility_Data_Form()
        # partner_choices = []
        # partner_choices.append(("", "-- select --"))
        # for i in Partners.objects.all():
        #     partner_choices.append((i.id, i.name))
        # form['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/update_facility.html', {'form': form, "title": "Add Facility",
                                                               "sub_title": "Add new Facility to your List",
                                                               'loggedin_user': loggedin_user})


# @login_required(login_url='/login/')
def view_facility_data(request, facility_id):
    if 'logged_in_username' not in request.session:
        return HttpResponseRedirect("/signup")

    facility = get_object_or_404(Facility_Info, pk=facility_id)

    facilitydata = Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county') \
        .select_related('sub_county').get(pk=facility_id)

    implementation_info = Implementation_type.objects.get(facility_info=facility_id)
    emr_info = EMR_Info.objects.select_related('type').get(facility_info=facility_id)
    hts_info = HTS_Info.objects.get(facility_info=facility_id)
    il_info = IL_Info.objects.get(facility_info=facility_id)
    mhealth_info = MHealth_Info.objects.get(facility_info=facility_id)

    initial_data = {  # 1st Method
        'mfl_code': facilitydata.mfl_code,
        'name': facilitydata.name,
        'county': facilitydata.county.name,
        'sub_county': facilitydata.sub_county.name,
        'owner': facilitydata.owner.name if facilitydata.owner else "",
        'partner': facilitydata.partner.name if facilitydata.partner else "None",
        'agency': facilitydata.partner.agency.name if facilitydata.partner and facilitydata.partner.agency else "None",
        'lat': facilitydata.lat,
        'lon': facilitydata.lon,
        'CT': implementation_info.ct,
        'HTS': implementation_info.hts,
        'IL':  implementation_info.il,
        'ovc_offered': emr_info.ovc,
        'otz_offered': emr_info.otz,
        'tb_offered': emr_info.tb,
        'prep_offered': emr_info.prep,
        'mnch_offered': emr_info.mnch,
        'kp_offered': emr_info.kp,
        'lab_man_offered': emr_info.lab_manifest,
        'mhealth_ushauri': mhealth_info.Ushauri,
        'mhealth_nishauri': mhealth_info.Nishauri,
        'mhealth_c4c': mhealth_info.C4C,
        'mhealth_mlab': mhealth_info.Mlab,
        'mhealth_psurvey': mhealth_info.Psurvey,
        'mhealth_art': mhealth_info.ART_Directory,
        'il_status': il_info.status,
        'webADT_registration': il_info.webADT_registration,
        'webADT_pharmacy': il_info.webADT_pharmacy,
        'il_three_PM': il_info.three_PM,
        'il_air': il_info.air,
        'il_ushauri': il_info.Ushauri,
        'il_mlab': il_info.Mlab,
        'emr_type': emr_info.type.type if emr_info.type else "",
        'emr_status': emr_info.status,
        'hts_use': hts_info.hts_use_name.hts_use_name if hts_info.hts_use_name else "",
        'hts_deployment': hts_info.deployment.deployment if hts_info.deployment else "",
        'hts_status': hts_info.status,
    }
    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/view_facility.html',
                  {'facilitydata': facilitydata,  "title": "Facility", "initial_data":initial_data,
                   "sub_title": "View facility details", 'loggedin_user': loggedin_user})


# @login_required(login_url='/login/')
def update_facility_data(request, facility_id):
    if 'logged_in_username' not in request.session:
        return HttpResponseRedirect("/signup")

    # does item exist in db
    facility = get_object_or_404(Facility_Info, pk=facility_id)

    facilitydata = Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county') \
        .select_related('sub_county').get(pk=facility_id)

    implementation_info = Implementation_type.objects.get(facility_info=facility_id)
    emr_info = EMR_Info.objects.select_related('type').get(facility_info=facility_id)
    hts_info = HTS_Info.objects.get(facility_info=facility_id)
    il_info = IL_Info.objects.get(facility_info=facility_id)
    mhealth_info = MHealth_Info.objects.get(facility_info=facility_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

        if form.is_valid():
            try:
                unique_id_for_edit = uuid.uuid4()

                # notify users of changes for approval ##### testing #####
                try:
                    org_partner = int(form.cleaned_data['partner'])
                    send_email(request.scheme, request.META['HTTP_HOST'], request.session['logged_in_username'], facility_id,
                               facilitydata.mfl_code, org_partner)
                except Exception as e:
                    print("Email error ----->", e)
                ##### testing #####

                # Save the new category to the database.
                facility = Edited_Facility_Info.objects.create(id=unique_id_for_edit,
                                                               mfl_code=form.cleaned_data['mfl_code'],
                                                               name=form.cleaned_data['name'],
                                                               county=Counties.objects.get(
                                                                   pk=int(form.cleaned_data['county'])),
                                                               sub_county=Sub_counties.objects.get(
                                                                   pk=int(form.cleaned_data['sub_county'])),
                                                               owner=Owner.objects.get(
                                                                   pk=int(form.cleaned_data['owner'])),
                                                               partner=Partners.objects.get(
                                                                   pk=int(form.cleaned_data['partner'])) if
                                                               form.cleaned_data['partner'] != "" else None,
                                                               # facilitydata.agency = facilitydata.partner.agency.name
                                                               lat=form.cleaned_data['lat'],
                                                               lon=form.cleaned_data['lon'],
                                                               facility_info=Facility_Info.objects.get(pk=facility_id),
                                                               date_edited=datetime.now(),
                                                               user_edited_name=request.session["logged_in_username"],
                                                                 user_edited_email = request.session["logged_in_user_email"]
                                                               )

                facility.save()

                # save Implementation info
                implementation_info = Implementation_type(ct=form.cleaned_data['CT'],
                                                          hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                          for_version="edited",
                                                          facility_edits=Edited_Facility_Info.objects.get(
                                                              pk=unique_id_for_edit))

                implementation_info.save()

                if form.cleaned_data['HTS'] == True:
                    # save HTS info
                    hts_info = HTS_Info(hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                        status=form.cleaned_data['hts_status'],
                                        deployment=HTS_deployment_type.objects.get(
                                            pk=int(form.cleaned_data['hts_deployment'])),
                                        for_version="edited",
                                        facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    hts_info.save()
                else:
                    # save HTS info
                    hts_info = HTS_Info(hts_use_name=None, status=None, deployment=None,
                                        for_version="edited",
                                        facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    hts_info.save()

                # save EMR info
                if form.cleaned_data['CT'] == True:
                    emr_info = EMR_Info(type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                                        status=form.cleaned_data['emr_status'],
                                        ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                                        prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                                        kp=form.cleaned_data['kp_offered'], mnch=form.cleaned_data['mnch_offered'],
                                        lab_manifest=form.cleaned_data['lab_man_offered'],
                                        for_version="edited",
                                        facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    emr_info.save()
                else:
                    emr_info = EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
                                        tb=None, kp=None, mnch=None, lab_manifest=None,
                                        for_version="edited",
                                        facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    emr_info.save()

                # save IL info
                print('webADT this', form.cleaned_data['webADT_registration'], form.cleaned_data['webADT_pharmacy'])
                if form.cleaned_data['IL'] == True:
                    il_info = IL_Info(webADT_registration=form.cleaned_data['webADT_registration'],
                                      webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                      status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['il_three_PM'],
                                      air=form.cleaned_data['il_air'], Ushauri=form.cleaned_data['il_ushauri'],
                                      Mlab=form.cleaned_data['il_mlab'],
                                      for_version="edited",
                                      facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    il_info.save()
                else:
                    il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                                      air=None, Ushauri=None, Mlab=None,
                                      for_version="edited",
                                      facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    il_info.save()

                # save MHealth info
                mhealth_info = MHealth_Info(Ushauri=form.cleaned_data['mhealth_ushauri'],
                                            C4C=form.cleaned_data['mhealth_c4c'],
                                            Nishauri=form.cleaned_data['mhealth_nishauri'],
                                            ART_Directory=form.cleaned_data['mhealth_art'],
                                            Psurvey=form.cleaned_data['mhealth_psurvey'],
                                            Mlab=form.cleaned_data['mhealth_mlab'],
                                            for_version="edited",
                                            facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                mhealth_info.save()

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS,
                                     'Facility was edited! Changes made to facility data will be approved before being shown below')
                return HttpResponseRedirect('/home')

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS,
                                     'Facility changes were saved. Waiting for approval before displaying them!')
                return HttpResponseRedirect('/home')

            except Exception as e:
                print("Error ----> ", e)
                messages.add_message(request, messages.ERROR,
                                     'A problem was encountered when submitting facility data. Please try again.')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:

        initial_data = {  # 1st Method
            'mfl_code': facilitydata.mfl_code,
            'name': facilitydata.name,
            'county': facilitydata.county.id,
            'sub_county': facilitydata.sub_county.id,
            'owner': facilitydata.owner.id if facilitydata.owner else "",
            'partner': facilitydata.partner.id if facilitydata.partner else "",
            'agency': facilitydata.partner.agency.name if facilitydata.partner and facilitydata.partner.agency else "",
            'lat': facilitydata.lat,
            'lon': facilitydata.lon,
            'CT': implementation_info.ct,
            'HTS': implementation_info.hts,
            'IL': implementation_info.il,
            'ovc_offered': emr_info.ovc,
            'otz_offered': emr_info.otz,
            'tb_offered': emr_info.tb,
            'prep_offered': emr_info.prep,
            'mnch_offered': emr_info.mnch,
            'kp_offered': emr_info.kp,
            'lab_man_offered': emr_info.lab_manifest,
            'mhealth_ushauri': mhealth_info.Ushauri,
            'mhealth_nishauri': mhealth_info.Nishauri,
            'mhealth_c4c': mhealth_info.C4C,
            'mhealth_mlab': mhealth_info.Mlab,
            'mhealth_psurvey': mhealth_info.Psurvey,
            'mhealth_art': mhealth_info.ART_Directory,
            'il_status': il_info.status,
            'webADT_registration': il_info.webADT_registration,
            'webADT_pharmacy': il_info.webADT_pharmacy,
            'il_three_PM': il_info.three_PM,
            'il_air': il_info.air,
            'il_ushauri': il_info.Ushauri,
            'il_mlab': il_info.Mlab,
            'emr_type': emr_info.type.id if emr_info.type else "",
            'emr_status': emr_info.status,
            'hts_use': hts_info.hts_use_name.id if hts_info.hts_use_name else "",
            'hts_deployment': hts_info.deployment.id if hts_info.deployment else "",
            'hts_status': hts_info.status,
        }
        form = Facility_Data_Form(initial=initial_data)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

    # check for edits
    try:
        facility_edits = Edited_Facility_Info.objects.get(facility_info=facility_id)
    except Edited_Facility_Info.DoesNotExist:
        facility_edits = None

    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/update_facility.html',
                  {'facilitydata': facilitydata, 'facility_edits': facility_edits,
                   'mhealth_info': mhealth_info, 'form': form, "title": "Update Facility data",
                   "sub_title": "Make changes to a Facility", 'loggedin_user': loggedin_user})


# from django.conf import settings
# @login_required(login_url='/login/')
def approve_facility_changes(request, facility_id):
    if 'logged_in_username' not in request.session:
        return HttpResponseRedirect("/signup")

    # does item exist in db
    facility_edits = get_object_or_404(Edited_Facility_Info, pk=facility_id)

    edited_facilitydata = Edited_Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county') \
        .select_related('sub_county').get(pk=facility_id)

    implementation_info = Implementation_type.objects.get(facility_edits=facility_id)
    emr_info = EMR_Info.objects.select_related('type').get(facility_edits=facility_id)
    hts_info = HTS_Info.objects.get(facility_edits=facility_id)
    il_info = IL_Info.objects.get(facility_edits=facility_id)
    mhealth_info = MHealth_Info.objects.get(facility_edits=facility_id)

    initial_facility_data = Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county') \
        .select_related('sub_county').get(pk=edited_facilitydata.facility_info.id)

    # compare changes
    compare_edits = compare_changes_made(initial_facility_data, edited_facilitydata)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

        if form.is_valid():
            try:
                if request.POST.get("approve"):
                    facility_to_edit = edited_facilitydata.facility_info.id
                    # Save the new category to the database.
                    Facility_Info.objects.filter(pk=facility_to_edit).update(mfl_code=form.cleaned_data['mfl_code'],
                                                                             name=form.cleaned_data['name'],
                                                                             county=Counties.objects.get(
                                                                                 pk=int(form.cleaned_data['county'])),
                                                                             sub_county=Sub_counties.objects.get(pk=int(
                                                                                 form.cleaned_data['sub_county'])),
                                                                             owner=Owner.objects.get(
                                                                                 pk=int(form.cleaned_data['owner'])),
                                                                             partner=Partners.objects.get(pk=int(
                                                                                 form.cleaned_data['partner'])) if
                                                                             form.cleaned_data[
                                                                                 'partner'] != "" else None,
                                                                             # facilitydata.agency = facilitydata.partner.agency.name
                                                                             lat=form.cleaned_data['lat'],
                                                                             lon=form.cleaned_data['lon'],
                                                                             )

                    Implementation_type.objects.filter(facility_info=facility_to_edit).update(
                        ct=form.cleaned_data['CT'], hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL']
                    )

                    # save HTS info
                    if form.cleaned_data['HTS'] == True:
                        HTS_Info.objects.filter(facility_info=facility_to_edit).update(
                            hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                            status=form.cleaned_data['hts_status'],
                            deployment=HTS_deployment_type.objects.get(pk=int(form.cleaned_data['hts_deployment'])))
                    else:
                        HTS_Info.objects.filter(facility_info=facility_to_edit).update(hts_use_name=None, status=None,
                                                                                       deployment=None)

                    # save EMR info
                    if form.cleaned_data['CT'] == True:
                        EMR_Info.objects.filter(facility_info=facility_to_edit).update(
                            type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                            status=form.cleaned_data['emr_status'],
                            ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                            prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                            kp=form.cleaned_data['kp_offered'], mnch=form.cleaned_data['mnch_offered'],
                            lab_manifest=form.cleaned_data['lab_man_offered'])
                    else:
                        EMR_Info.objects.filter(facility_info=facility_to_edit).update(type=None, status=None, ovc=None,
                                                                                       otz=None, prep=None,
                                                                                       tb=None, kp=None, mnch=None,
                                                                                       lab_manifest=None, )

                    # save IL info
                    if form.cleaned_data['IL'] == True:
                        IL_Info.objects.filter(facility_info=facility_to_edit).update(
                            webADT_registration=form.cleaned_data['webADT_registration'],
                            webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                            status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['il_three_PM'],
                                      air=form.cleaned_data['il_air'], Ushauri=form.cleaned_data['il_ushauri'],
                                      Mlab=form.cleaned_data['il_mlab'])
                    else:
                        IL_Info.objects.filter(facility_info=facility_to_edit).update(
                            webADT_registration=None, webADT_pharmacy=None, status=None,
                            three_PM=None,
                                      air=None, Ushauri=None,
                                      Mlab=None
                        )

                    # save MHealth info
                    MHealth_Info.objects.filter(facility_info=facility_to_edit).update(
                        Ushauri=form.cleaned_data['mhealth_ushauri'],
                        C4C=form.cleaned_data['mhealth_c4c'],
                        Nishauri=form.cleaned_data['mhealth_nishauri'],
                        ART_Directory=form.cleaned_data['mhealth_art'],
                        Psurvey=form.cleaned_data['mhealth_psurvey'],
                        Mlab=form.cleaned_data['mhealth_mlab']
                    )

                # delete all edits of this facility whether approved or discarded
                Implementation_type.objects.get(facility_edits=facility_id).delete()
                HTS_Info.objects.get(facility_edits=facility_id).delete()
                EMR_Info.objects.get(facility_edits=facility_id).delete()
                IL_Info.objects.get(facility_edits=facility_id).delete()
                MHealth_Info.objects.get(facility_edits=facility_id).delete()
                Edited_Facility_Info.objects.get(pk=facility_id).delete()

                # Finally redirect to home (/)
                show0message = 'Changes were approved and merged successfully!' if request.POST.get(
                    "approve") else 'Changes were discarded successfully!'
                messages.add_message(request, messages.SUCCESS, show0message)
                return HttpResponseRedirect('/home')

            except Exception as e:
                messages.add_message(request, messages.ERROR,
                                     'A problem was encountered when submitting facility data. Please try again.')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        initial_data = {  # 1st Method
            'mfl_code': edited_facilitydata.mfl_code,
            'name': edited_facilitydata.name,
            'county': edited_facilitydata.county.id,
            'sub_county': edited_facilitydata.sub_county.id,
            'owner': edited_facilitydata.owner.id,
            'partner': edited_facilitydata.partner.id if edited_facilitydata.partner else "",
            'agency': edited_facilitydata.partner.agency.name if edited_facilitydata.partner and edited_facilitydata.partner.agency else "",
            'lat': edited_facilitydata.lat,'lon': edited_facilitydata.lon,
            'CT': implementation_info.ct, 'HTS': implementation_info.hts, 'IL': implementation_info.il,
            'ovc_offered': emr_info.ovc,
            'otz_offered': emr_info.otz,
            'tb_offered': emr_info.tb,
            'prep_offered': emr_info.prep,
            'mnch_offered': emr_info.mnch,
            'kp_offered': emr_info.kp,
            'lab_man_offered': emr_info.lab_manifest,
            'mhealth_ushauri': mhealth_info.Ushauri,
            'mhealth_nishauri': mhealth_info.Nishauri,
            'mhealth_c4c': mhealth_info.C4C,
            'mhealth_mlab': mhealth_info.Mlab,
            'mhealth_psurvey': mhealth_info.Psurvey,
            'mhealth_art': mhealth_info.ART_Directory,
            'il_status': il_info.status,
            'webADT_registration': il_info.webADT_registration,
            'webADT_pharmacy': il_info.webADT_pharmacy,
            'il_three_PM': il_info.three_PM,
            'il_air': il_info.air,
            'il_ushauri': il_info.Ushauri,
            'il_mlab': il_info.Mlab,
            'emr_type': emr_info.type.id if emr_info.type else "",
            'emr_status': emr_info.status,
            'hts_use': hts_info.hts_use_name.id if hts_info.hts_use_name else "",
            'hts_deployment': hts_info.deployment.id if hts_info.deployment else "",
            'hts_status': hts_info.status,
        }
        form = Facility_Data_Form(initial=initial_data)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in
                                                          Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices = [("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in
                                                              HTS_deployment_type.objects.all()]

    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/update_facility.html',
                  {'facilitydata': edited_facilitydata, 'form': form, "title": "Changes Awaiting Approval",
                   "sub_title": "Approve or reject the changes made to the facility", 'loggedin_user': loggedin_user,
                   "compare_edits":compare_edits})


def compare_changes_made(initial_facility_data, edited_facilitydata):
    implementation_info = Implementation_type.objects.get(facility_edits=edited_facilitydata.id)
    emr_info = EMR_Info.objects.select_related('type').get(facility_edits=edited_facilitydata.id)
    hts_info = HTS_Info.objects.get(facility_edits=edited_facilitydata.id)
    il_info = IL_Info.objects.get(facility_edits=edited_facilitydata.id)
    mhealth_info = MHealth_Info.objects.get(facility_edits=edited_facilitydata.id)

    initial_implementation_info = Implementation_type.objects.get(facility_info=initial_facility_data.id)
    initial_emr_info = EMR_Info.objects.select_related('type').get(facility_info=initial_facility_data.id)
    initial_hts_info = HTS_Info.objects.get(facility_info=initial_facility_data.id)
    initial_il_info = IL_Info.objects.get(facility_info=initial_facility_data.id)
    initial_mhealth_info = MHealth_Info.objects.get(facility_info=initial_facility_data.id)

    compare_changes = {  # 1st Method
        'mfl_code': "edited" if edited_facilitydata.mfl_code != initial_facility_data.mfl_code else "no changes",
        'name': "edited" if edited_facilitydata.name != initial_facility_data.name else "no changes",
        'county': "edited" if edited_facilitydata.county.id != initial_facility_data.county.id else "no changes",
        'sub_county': "edited" if edited_facilitydata.sub_county.id != initial_facility_data.sub_county.id else "no changes",
        'owner': "edited" if edited_facilitydata.owner.id != initial_facility_data.owner.id else "no changes",
        'partner': "edited" if edited_facilitydata.partner.id  != initial_facility_data.partner.id  else "no changes",
        'agency': "edited" if edited_facilitydata.partner.agency.name  != initial_facility_data.partner.agency.name else "no changes",
        'lat': "edited" if edited_facilitydata.lat != initial_facility_data.lat else "no changes",
        'lon':"edited" if  edited_facilitydata.lon != initial_facility_data.lon else "no changes",
        'CT': "edited" if implementation_info.ct != initial_implementation_info.ct else "no changes",
        'HTS': "edited" if implementation_info.hts != initial_implementation_info.hts else "no changes",
        'IL': "edited" if implementation_info.il != initial_implementation_info.il else "no changes",
        'ovc_offered': "edited" if emr_info.ovc != initial_emr_info.ovc else "no changes",
        'otz_offered': "edited" if emr_info.otz != initial_emr_info.otz else "no changes",
        'tb_offered': "edited" if emr_info.tb != initial_emr_info.tb else "no changes",
        'prep_offered':"edited" if emr_info.prep != initial_emr_info.prep else "no changes",
        'mnch_offered': "edited" if emr_info.mnch != initial_emr_info.mnch else "no changes",
        'kp_offered': "edited" if emr_info.kp != initial_emr_info.kp else "no changes",
        # 'lab_man_offered': emr_info.lab_manifest,
        # 'mhealth_ushauri': mhealth_info.Ushauri,
        # 'mhealth_nishauri': mhealth_info.Nishauri,
        # 'mhealth_c4c': mhealth_info.C4C,
        # 'mhealth_mlab': mhealth_info.Mlab,
        # 'mhealth_psurvey': mhealth_info.Psurvey,
        # 'mhealth_art': mhealth_info.ART_Directory,
        # 'il_status': il_info.status,
        # 'webADT_registration': il_info.webADT_registration,
        # 'webADT_pharmacy': il_info.webADT_pharmacy,
        # 'il_three_PM': il_info.three_PM,
        # 'il_air': il_info.air,
        # 'il_ushauri': il_info.Ushauri,
        # 'il_mlab': il_info.Mlab,
        # 'emr_type': emr_info.type.id if emr_info.type else "",
        # 'emr_status': emr_info.status,
        # 'hts_use': hts_info.hts_use_name.id if hts_info.hts_use_name else "",
        # 'hts_deployment': hts_info.deployment.id if hts_info.deployment else "",
        # 'hts_status': hts_info.status,
    }
    return compare_changes


def delete_facility(request, facility_id):

    # get rid of the edits
    try:
        Edited_Facility_Info.objects.get(facility_info=facility_id).delete()
    except Edited_Facility_Info.DoesNotExist:
        print('Edited facility doesnt exist')

    # # get rid of the facility
    # Implementation_type.objects.get(facility_info=facility_id).delete() if Implementation_type.objects.get(facility_info=facility_id) else ""
    # HTS_Info.objects.get(facility_info=facility_id).delete() if HTS_Info.objects.get(facility_info=facility_id) else ""
    # EMR_Info.objects.get(facility_info=facility_id).delete() if EMR_Info.objects.get(facility_info=facility_id) else ""
    # IL_Info.objects.get(facility_info=facility_id).delete() if IL_Info.objects.get(facility_info=facility_id) else ""
    # MHealth_Info.objects.get(facility_info=facility_id).delete() if MHealth_Info.objects.get(facility_info=facility_id) else ""
    Facility_Info.objects.get(pk=facility_id).delete()

    # messages.add_message(request, messages.SUCCESS, "Facility successfully deleted!")
    return HttpResponseRedirect('/home')


# @login_required(login_url='/login/')
def partners(request):
    if 'logged_in_username' not in request.session:
        return HttpResponseRedirect("/signup")

    partners_data = Partners.objects.prefetch_related('agency').all()

    if request.method == 'POST':
        try:
            Partners.objects.filter(pk=int(request.POST.get('partner_id'))) \
                .update(name=request.POST.get('partner'),
                        agency=SDP_agencies.objects.get(pk=int(request.POST.get('agency'))))
            messages.add_message(request, messages.SUCCESS, 'Updated Partners nd agencies data. View changes below!')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'An error occured. Please try again!')

    loggedin_user = request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/partners_list.html', {'partners_data': partners_data, 'loggedin_user': loggedin_user})


def sub_counties(request):
    # sub_counties = Sub_counties.objects.filter(county=county_id)
    # data = serialize("json", sub_counties)
    # return HttpResponse(data, content_type="application/json")
    counties = Counties.objects.all()

    sub_counties_list = []
    for row in counties:
        sub_counties = Sub_counties.objects.filter(county=row.id).order_by('name')

        subObj = {}
        subObj['county'] = row.id
        subObj['sub_county'] = [{'id': sub.id, 'name': sub.name} for sub in sub_counties]

        sub_counties_list.append(subObj)

    return JsonResponse(sub_counties_list, safe=False)


def get_partners_list(request):
    partners = Partners.objects.select_related('agency').all()

    partners_list = []
    for row in partners:
        partnerObj = {}
        partnerObj['partner'] = row.id
        partnerObj['agency'] = {'id': row.agency.id, 'name': row.agency.name} if row.agency else {}

        partners_list.append(partnerObj)

    return JsonResponse(partners_list, safe=False)


def get_agencies_list(request):
    agencies = SDP_agencies.objects.all()

    agencies_list = []
    for row in agencies:
        agencyObj = {}
        agencyObj['id'] = row.id
        agencyObj['name'] = row.name

        agencies_list.append(agencyObj)

    return JsonResponse(agencies_list, safe=False)


@csrf_exempt
def get_mfl_data(request):
    facilityObj = {}

    if request.method == 'POST':
        try:

            try:
                Facility_Info.objects.get(mfl_code=int(request.POST.get('code')))
                facilityObj = {"status": 'data exists'}
            except Facility_Info.DoesNotExist:
                mfl_data = Master_Facility_List.objects.select_related('county').select_related('sub_county')\
                    .select_related('partner').select_related('owner').get(mfl_code=int(request.POST.get('code')))

                print('code posted from form, ', request.POST.get('code'))

                facilityObj['mfl_code'] = mfl_data.mfl_code
                facilityObj['name'] = mfl_data.name
                facilityObj['county'] = mfl_data.county.id
                facilityObj['sub_county'] = mfl_data.sub_county.id
                facilityObj['lat'] = float(mfl_data.lat) if mfl_data.lat else ""
                facilityObj['lon'] = float(mfl_data.lon) if mfl_data.lon else ""
                facilityObj['partner'] = mfl_data.partner.id if mfl_data.partner else ""
                facilityObj['owner'] = mfl_data.owner.id
                facilityObj['agency'] = mfl_data.partner.agency.name if mfl_data.partner else ""
        except Edited_Facility_Info.DoesNotExist:
            print(request.POST.get('code'), ' doesn\'t exist')

    return JsonResponse(facilityObj, safe=False)


from django.http import FileResponse
from openpyxl.chart import BarChart,Reference
def convert_to_excel(request):
    facilities_info = Facility_Info.objects.prefetch_related('partner') \
        .select_related('county') \
        .select_related('sub_county').all()

    facilitiesdata = []

    for row in facilities_info:
        implementation_info = Implementation_type.objects.get(facility_info=row.id)
        emr_info = EMR_Info.objects.get(facility_info=row.id)
        hts_info = HTS_Info.objects.get(facility_info=row.id)
        il_info = IL_Info.objects.get(facility_info=row.id)
        mhealth_info = MHealth_Info.objects.get(facility_info=row.id)

        ct = "CT" if implementation_info.ct else ""
        hts = "HTS" if implementation_info.hts else ""
        il = "IL" if implementation_info.il else ""

        implementation = [ct, hts, il]

        dataObj = {}
        dataObj["id"] = row.id
        dataObj["mfl_code"] = row.mfl_code
        dataObj["name"] = row.name
        dataObj["county"] = row.county.name
        dataObj["sub_county"] = row.sub_county.name
        dataObj["owner"] = row.owner.name if row.owner else ""
        dataObj["lat"] = row.lat if row.lat else ""
        dataObj["lon"] = row.lon if row.lon else ""
        dataObj["partner"] = row.partner.name if row.partner else ""
        dataObj["agency"] = row.partner.agency.name if row.partner and row.partner.agency else ""
        dataObj["implementation"] = implementation
        dataObj["emr_type"] = emr_info.type.type if emr_info.type else ""
        dataObj["emr_status"] = emr_info.status if emr_info.status else ""
        dataObj["hts_use"] = hts_info.hts_use_name.hts_use_name if hts_info.hts_use_name else ""
        dataObj["hts_deployment"] = hts_info.deployment.deployment if hts_info.deployment else ""
        dataObj["hts_status"] = hts_info.status
        dataObj["il_status"] = il_info.status
        dataObj["il_registration_ie"] = il_info.webADT_registration
        dataObj["il_pharmacy_ie"] = il_info.webADT_pharmacy
        dataObj["mhealth_ovc"] = mhealth_info.Nishauri

        facilitiesdata.append(dataObj)

    # workbook = xlsxwriter.Workbook('HIS Master List.xlsx')
    #
    # # By default worksheet names in the spreadsheet will be
    # # Sheet1, Sheet2 etc., but we can also specify a name.
    # worksheet = workbook.add_worksheet("HIF List")
    #
    # #add your titles
    # worksheet.write(0, 0, "mfl_code")
    # worksheet.write(0, 1, "name")
    # worksheet.write(0, 3, "county")
    # worksheet.write(0, 4, "sub_county")
    # worksheet.write(0, 5, "owner")
    # worksheet.write(0, 6, "lat")
    # worksheet.write(0, 7, "lon")
    #
    # # Start from the first cell. Rows
    # row = 1
    #
    # # Iterate over the data and write it out row by row.
    # for data in (facilitiesdata):
    #     worksheet.write(row, 0, data["mfl_code"])
    #     worksheet.write(row, 1, data["name"])
    #     worksheet.write(row, 3, data["county"])
    #     worksheet.write(row, 4, data["sub_county"])
    #     worksheet.write(row, 5, data["owner"])
    #     worksheet.write(row, 6, data["lat"])
    #     worksheet.write(row, 7, data["lon"])
    #     row += 1
    #
    # # data = (['me', 21], ['steven', 32], ['carl', 6])
    # data = [1,2,5,3,6,8,12]
    # # create data for plotting
    # values = Reference(data, min_col=1, min_row=1,
    #                    max_col=1, max_row=10)
    #
    # # Create object of BarChart class
    # chart = BarChart()
    #
    # # adding data to the Bar chart object
    # chart.add_data(values)
    #
    # # set the title of the chart
    # chart.title = " BAR-CHART "
    #
    # # set the title of the x-axis
    # chart.x_axis.title = " X_AXIS "
    #
    # # set the title of the y-axis
    # chart.y_axis.title = " Y_AXIS "
    #
    # # add chart to the sheet
    # # the top-left corner of a chart
    # # is anchored to cell E2 .
    # worksheet.add_chart(chart, "J2")
    #
    # workbook.close()
    #
    # file = open('HIS Master List.xlsx', 'rb')
    # response = FileResponse(file)
    return facilitiesdata



from django.db.models import Count

def charts(request):
    result = EMR_Info.objects.annotate(count=Count('author'))

    return result