from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import uuid
import mysql.connector
from django.contrib.auth.decorators import login_required

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

from django.conf import settings

from .models import *
from .forms.facilities.forms import *

from requests.structures import CaseInsensitiveDict
import requests
import json


def test_email(request):
    demain = request.META['HTTP_HOST']
    print("domain", demain, request.scheme)
    print(request.scheme + request.META['HTTP_HOST'] + '/facilities/update_facility/'+'981893d7-8488-4319-b976-747873551b71')
    context = {
        'news': 'We have good news!',
        'url': request.scheme + "://" + request.META['HTTP_HOST'] + '/facilities/update_facility/' ,
        'mfl_code': 122345, #facilitydata.mfl_code,
        'facility_id': '981893d7-8488-4319-b976-747873551b71', #facilitydata.id
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
        'mfl_code': mfl_code, #facilitydata.mfl_code,
        'facility_id': facility_id, #facilitydata.id
        'username': user_names
    }
    organization = Organization_stewards.objects.get(organization=partner_id)

    msg_html = render_to_string('facilities/email_template.html', context)
    msg = EmailMessage(subject="Facility Modified", body=msg_html, from_email=settings.DEFAULT_FROM_EMAIL,
                       bcc=['marykilewe@gmail.com', organization.email])#, organization.email
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    print('-----------> sending mail ...', organization.email)
    return 0


from django.views.decorators.csrf import csrf_exempt,csrf_protect
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

        edits = Edited_Facility_Info.objects.select_related('user_edited').get(facility_info=facility_id)
        # user = User.objects.get(pk=edits.user_edited)
        print("the user is", edits.user_edited.first_name)

        context = {
            'news': 'We have good news!',
            'url': request.scheme + "://" + request.META['HTTP_HOST'] + '/facilities/update_facility/',
            'mfl_code':facilitydata.mfl_code,
            'facility_id': facilitydata.id,
            "message_title": message_title,
            "reason_given":reason,
            "choice": choice,
            "message": message,
            "user_name": edits.user_edited.first_name + " "+ edits.user_edited.last_name
        }
        msg_html = render_to_string('facilities/customizable_email.html', context)
        msg = EmailMessage(subject=subject, body=msg_html, from_email=settings.DEFAULT_FROM_EMAIL,
                           bcc=[edits.user_edited.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print('-----------> sending customized mail ...', choice)
    return HttpResponse(0)


def add_stewards(request):

    # file = os.path.join(Path(__file__).resolve().parent.parent, "facilities/kenyahmis_stewards.xlsx")
    # stewards_data = pd.read_excel(file)  # reading file
    #make json sheet of excel file
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
        #Partners.objects.create(name=stewardObj[2]).save()
        Organization_stewards.objects.create(steward=stewardObj[1], organization=Partners.objects.get(name=stewardObj[2]),
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
    excel_facilities = pd.read_excel(file, sheet_name='Fridah')  # reading file

    for i in range(0, 632): #data['total_pages']:
        try:
            Partners.objects.get_or_create(name=(excel_facilities['SDP'][i]).strip(),
                     agency=SDP_agencies.objects.get(name=(excel_facilities['SDP Agency'][i]).strip()))
        except Exception as e:
            print(excel_facilities['SDP'][i])
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

    for i in range(2, 420): #data['total_pages']
        url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json&page='+ str(i)
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
    #fetch data from excel sheet saved as json
    f = open(os.path.join(Path(__file__).resolve().parent.parent, "facilites_from_excel.json"), 'r')
    excel_facilities = json.load(f)

    # fetch data from kmhfl api
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer Co5oG8q1RJMnjuXrqunEyPg6iV5s3M"
    url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json'
    response = requests.get(url, headers=headers)

    data = json.loads(response.content)

    for i in range(2, 420): #data['total_pages']
        #print("Page on ", i)
        next_url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json&page='+ str(i)
        next_page_response = requests.get(next_url, headers=headers)

        next_page_data = json.loads(next_page_response.content)

        for i in range(0, len(next_page_data['results'])):
            # loop through facilities in file and search page for it
            for fac in excel_facilities:
                #print(next(iter(fac.keys())))
                if int(next(iter(fac.keys()))) == next_page_data['results'][i]['code']:
                    print("Found --->",next_page_data['results'][i]['code'], "-----> Page :", i)
                    fill_database(next_page_data['results'][i], next(iter(fac.values())))
    return 0


def fill_database(kmhfl_facility, excel_facility):
    print('=========================================================')
    print(kmhfl_facility['code'], kmhfl_facility['name'], kmhfl_facility['county_name'], kmhfl_facility['sub_county_name'],
          kmhfl_facility['owner_type_name'], kmhfl_facility["lat_long"])
    print('/////////////////////////////////////////////////////')
    #CT, HTS, IL = excel_facility['implementation'].split(' & ')
    print('=========================================================')

    lat_long = kmhfl_facility["lat_long"] if kmhfl_facility["lat_long"] else [None, None]
    unique_facility_id = uuid.uuid4()

    Facility_Info.objects.create(id=unique_facility_id, mfl_code=kmhfl_facility['code'],
                                            name=kmhfl_facility['name'],
                                            county=Counties.objects.get(name=kmhfl_facility['county_name']),
                                            sub_county=Sub_counties.objects.get(
                                                name=kmhfl_facility['sub_county_name']),
                                            owner=Owner.objects.get(name=kmhfl_facility['owner_type_name']),
                                            partner=Partners.objects.get(name=excel_facility['partner']),
                                            lat=lat_long[0],
                                            lon=lat_long[1],
                                            kmhfltest_id=kmhfl_facility["id"]
                                            ).save()

    # save Implementation info
    CT = True if 'CT' in excel_facility['implementation'] else False
    HTS = True if 'HTS' in excel_facility['implementation'] else False
    IL = True if 'IL' in excel_facility['implementation'] else False
    Implementation_type(ct=CT, hts=HTS, il=IL,
                                              for_version="original",
                                              facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

    # save HTS info
    if HTS:
        HTS_Info(hts_use_name=HTS_use_type.objects.get(hts_use_name=excel_facility['hts_use']),
                            status=excel_facility['hts_status'],
                            deployment=HTS_deployment_type.objects.get(deployment=excel_facility['hts_deployment']),
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
        EMR_Info(type=EMR_type.objects.get(type=excel_facility['emr']), status=excel_facility['emr_status'],
                 ovc=change_value(excel_facility['OVC']), otz=change_value(excel_facility['OTZ']), prep=change_value(excel_facility['PrEP']),
                 tb=change_value(excel_facility['TB']), kp=change_value(excel_facility['KP']), mnch=change_value(excel_facility['MCH']),
                 lab_manifest=change_value(excel_facility['Lab Manifest']),
                 for_version="original", facility_edits=None,
                 facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
    else:
        EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
                            tb=None, kp=None, mnch=None, lab_manifest=None,
                            for_version="original", facility_edits=None,
                            facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

    # save IL info
    if IL:
        IL_Info(webADT_registration=change_value(excel_facility['webADT_registration']), webADT_pharmacy=change_value(excel_facility['webADT_pharmacy']),
                status=excel_facility['il_status'], three_PM=change_value(excel_facility['3PM']),
                for_version="original", facility_edits=None,
                facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
    else:
        IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                      for_version="original", facility_edits=None,
                      facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()

    # save MHealth info
    MHealth_Info(Ushauri=change_value(excel_facility['Ushauri']), C4C=None,
                Nishauri=change_value(excel_facility['Nishauri']), ART_Directory=None,
                Psurvey=None, Mlab=change_value(excel_facility['mlab']),
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















def index(request):

    #facilitydata = Facilities.objects.select_related('implementation').get(pk=1)
    facilities_info = Facility_Info.objects.prefetch_related('partner')\
                                                        .select_related('county') \
                                                        .select_related('sub_county').all()

    #implementation_info = Implementation_type.objects.select_related('facility_info').all()

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
        #return HttpResponseRedirect('/home')

    loggedin_user =request.session["logged_in_username"] if 'logged_in_username' in request.session else None
    return render(request, 'facilities/facilities_list.html', {'facilitiesdata': facilitiesdata,
                                                               'loggedin_user':loggedin_user})


@login_required(login_url='/login/')
def add_sub_counties(request):
    if request.method == 'POST':
        form = Sub_Counties_Form(request.POST)
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))

        if form.is_valid():
            subcounty = Sub_counties(name=(form.cleaned_data['add_sub_county']).strip(),
                                county=Counties.objects.get(pk=int(form.cleaned_data['county']))).save()
            messages.add_message(request, messages.SUCCESS, 'Sub county was successfully added and can be viewed below!')
            return HttpResponseRedirect('/facilities/add_sub_counties')
    else:
        form = Sub_Counties_Form()
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))

    return render(request, 'facilities/add_sub_counties.html', {'form': form, "title": "Add sub_counties"})


@login_required(login_url='/login/')
def add_facility_data(request):
    # if 'logged_in_username' not in request.session:
    #     return HttpResponseRedirect("/signup")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in Sub_counties.objects.all().order_by('name')]
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
                facility = Facility_Info.objects.create(id=unique_facility_id, mfl_code = form.cleaned_data['mfl_code'],
                    name = form.cleaned_data['name'],
                    county = Counties.objects.get(pk=int(form.cleaned_data['county'])),
                    sub_county = Sub_counties.objects.get(pk=int(form.cleaned_data['sub_county'])),
                    owner = Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                    partner = Partners.objects.get(pk=int(form.cleaned_data['partner'])) if form.cleaned_data['partner'] != "" else None,
                    #facilitydata.agency = facilitydata.partner.agency.name
                    lat = form.cleaned_data['lat'],
                    lon = form.cleaned_data['lon']
                )

                facility.save()

                # save Implementation info
                implementation_info = Implementation_type(ct=form.cleaned_data['CT'],
                                                            hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                          for_version="original",
                                                          facility_info=Facility_Info.objects.get(pk=unique_facility_id))

                implementation_info.save()

                if form.cleaned_data['HTS'] == True:
                    # save HTS info
                    hts_info = HTS_Info(hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                        status=form.cleaned_data['hts_status'],
                                          deployment=HTS_deployment_type.objects.get(pk=int(form.cleaned_data['hts_deployment'])),
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
                    il_info = IL_Info(webADT_registration=form.cleaned_data['webADT_registration'], webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                       status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['three_PM'],
                                       for_version="original",
                                       facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    il_info.save()
                else:
                    il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                                      for_version="original",
                                      facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                    il_info.save()

                # save MHealth info
                mhealth_info = MHealth_Info(Ushauri=form.cleaned_data['ushauri'], C4C=form.cleaned_data['c4c'],
                                   Nishauri=form.cleaned_data['nishauri'], ART_Directory=form.cleaned_data['art'],
                                            Psurvey=form.cleaned_data['psurvey'], Mlab=form.cleaned_data['mlab'],
                                            for_version="original",
                                            facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                mhealth_info.save()

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS, 'Facility was successfully added and can be viewed below!')
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
        #form['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['county'].choices = [("", "")] + [(i.id, i.name) for i in Counties.objects.all().order_by('name')]
        form.fields['sub_county'].choices = [("", "")] + [(i.id, i.name) for i in Sub_counties.objects.all().order_by('name')]
        form.fields['owner'].choices = [("", "")] + [(i.id, i.name) for i in Owner.objects.all()]
        form.fields['partner'].choices = [("", "")] + [(i.id, i.name) for i in Partners.objects.all()]
        form.fields['emr_type'].choices =[("", "")] + [(i.id, i.type) for i in EMR_type.objects.all()]
        form.fields['hts_use'].choices = [("", "")] + [(i.id, i.hts_use_name) for i in HTS_use_type.objects.all()]
        form.fields['hts_deployment'].choices = [("", "")] + [(i.id, i.deployment) for i in HTS_deployment_type.objects.all()]

    return render(request, 'facilities/update_facility.html', {'form': form, "title":"Add Facility"})


@login_required(login_url='/login/')
def update_facility_data(request, facility_id):
    # if 'logged_in_username' not in request.session:
    #     return HttpResponseRedirect("/signup")

    # does item exist in db
    facility = get_object_or_404(Facility_Info, pk=facility_id)

    facilitydata = Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county')\
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
                    current_users_name =request.user.first_name + " " + request.user.last_name
                    org_partner = int(form.cleaned_data['partner'])
                    send_email(request.scheme, request.META['HTTP_HOST'], current_users_name, facility_id,
                               facilitydata.mfl_code, org_partner)
                except Exception as e:
                    print("Email error ----->", e)
                ##### testing #####

                # Save the new category to the database.
                facility = Edited_Facility_Info.objects.create(id=unique_id_for_edit, mfl_code=form.cleaned_data['mfl_code'],
                                                        name=form.cleaned_data['name'],
                                                        county=Counties.objects.get(pk=int(form.cleaned_data['county'])),
                                                        sub_county=Sub_counties.objects.get(
                                                            pk=int(form.cleaned_data['sub_county'])),
                                                        owner=Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                                                        partner=Partners.objects.get(pk=int(form.cleaned_data['partner'])) if form.cleaned_data['partner'] != "" else None,
                                                        # facilitydata.agency = facilitydata.partner.agency.name
                                                        lat=form.cleaned_data['lat'],
                                                        lon=form.cleaned_data['lon'],
                                                               facility_info=Facility_Info.objects.get(pk=facility_id),
                                                               date_edited=datetime.now(),
                                                                user_edited = User.objects.get(pk=request.user.id)
                                                        )

                facility.save()

                # save Implementation info
                implementation_info = Implementation_type(ct=form.cleaned_data['CT'],
                                                          hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                          for_version="edited",
                                                          facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))

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
                                      status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['three_PM'],
                                      for_version="edited",
                                      facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    il_info.save()
                else:
                    il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                                      for_version="edited",
                                      facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                    il_info.save()

                # save MHealth info
                mhealth_info = MHealth_Info(Ushauri=form.cleaned_data['ushauri'], C4C=form.cleaned_data['c4c'],
                                            Nishauri=form.cleaned_data['nishauri'], ART_Directory=form.cleaned_data['art'],
                                            Psurvey=form.cleaned_data['psurvey'], Mlab=form.cleaned_data['mlab'],
                                            for_version="edited",
                                            facility_edits=Edited_Facility_Info.objects.get(pk=unique_id_for_edit))
                mhealth_info.save()

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS, 'Facility was edited! Changes made to facility data will be approved before being shown below')
                return HttpResponseRedirect('/home')

                # Redirect to home (/)
                messages.add_message(request, messages.SUCCESS, 'Facility changes were saved. Waiting for approval before displaying them!')
                return HttpResponseRedirect('/home')

            except Exception as e:
                print("Error ----> ",e)
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
            'ushauri': mhealth_info.Ushauri,
            'nishauri': mhealth_info.Nishauri,
            'c4c': mhealth_info.C4C,
            'mlab': mhealth_info.Mlab,
            'psurvey': mhealth_info.Psurvey,
            'art': mhealth_info.ART_Directory,
            'il_status': il_info.status,
            'webADT_registration': il_info.webADT_registration,
            'webADT_pharmacy': il_info.webADT_pharmacy,
            'three_PM': il_info.three_PM,
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
    return render(request, 'facilities/update_facility.html', {'facilitydata': facilitydata, 'facility_edits':facility_edits,
                                                               'mhealth_info':mhealth_info, 'form': form, "title":"Facility data"})


from django.conf import settings
@login_required(login_url='/login/')
def approve_facility_changes(request, facility_id):
    # if 'logged_in_username' not in request.session:
    #     return HttpResponseRedirect("/signup")

    # does item exist in db
    facility_edits = get_object_or_404(Edited_Facility_Info, pk=facility_id)

    edited_facilitydata = Edited_Facility_Info.objects.prefetch_related('partner') \
        .select_related('owner').select_related('county')\
        .select_related('sub_county').get(pk=facility_id)

    implementation_info = Implementation_type.objects.get(facility_edits=facility_id)
    emr_info = EMR_Info.objects.select_related('type').get(facility_edits=facility_id)
    hts_info = HTS_Info.objects.get(facility_edits=facility_id)
    il_info = IL_Info.objects.get(facility_edits=facility_id)
    mhealth_info = MHealth_Info.objects.get(facility_edits=facility_id)
    print('well well lookie here ', il_info.webADT_pharmacy, il_info.webADT_registration)

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
                    Facility_Info.objects.filter(pk=facility_to_edit).update(mfl_code = form.cleaned_data['mfl_code'],
                        name = form.cleaned_data['name'],
                        county = Counties.objects.get(pk=int(form.cleaned_data['county'])),
                        sub_county = Sub_counties.objects.get(pk=int(form.cleaned_data['sub_county'])),
                        owner = Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                        partner = Partners.objects.get(pk=int(form.cleaned_data['partner'])) if form.cleaned_data['partner'] != "" else None,
                        #facilitydata.agency = facilitydata.partner.agency.name
                        lat = form.cleaned_data['lat'],
                        lon = form.cleaned_data['lon'],
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
                        HTS_Info.objects.filter(facility_info=facility_to_edit).update(hts_use_name=None, status=None, deployment=None)

                    # save EMR info
                    if form.cleaned_data['CT'] == True:
                        EMR_Info.objects.filter(facility_info=facility_to_edit).update(type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                                            status=form.cleaned_data['emr_status'],
                                            ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                                            prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                                            kp=form.cleaned_data['kp_offered'], mnch=form.cleaned_data['mnch_offered'],
                                            lab_manifest=form.cleaned_data['lab_man_offered'])
                    else:
                        EMR_Info.objects.filter(facility_info=facility_to_edit).update(type=None, status=None, ovc=None, otz=None, prep=None,
                                                                tb=None, kp=None, mnch=None, lab_manifest=None,)

                    # save IL info
                    if form.cleaned_data['IL'] == True:
                        IL_Info.objects.filter(facility_info=facility_to_edit).update(webADT_registration=form.cleaned_data['webADT_registration'],
                                          webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                          status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['three_PM'])
                    else:
                        IL_Info.objects.filter(facility_info=facility_to_edit).update(webADT_registration=None, webADT_pharmacy=None,
                                                                                 status=None, three_PM=None)

                    # save MHealth info
                    MHealth_Info.objects.filter(facility_info=facility_to_edit).update(Ushauri=form.cleaned_data['ushauri'], C4C=form.cleaned_data['c4c'],
                                                Nishauri=form.cleaned_data['nishauri'], ART_Directory=form.cleaned_data['art'],
                                                Psurvey=form.cleaned_data['psurvey'], Mlab=form.cleaned_data['mlab'])

                # delete all edits of this facility whether approved or discarded
                Implementation_type.objects.get(facility_edits=facility_id).delete()
                HTS_Info.objects.get(facility_edits=facility_id).delete()
                EMR_Info.objects.get(facility_edits=facility_id).delete()
                IL_Info.objects.get(facility_edits=facility_id).delete()
                MHealth_Info.objects.get(facility_edits=facility_id).delete()
                Edited_Facility_Info.objects.get(pk=facility_id).delete()

                # Finally redirect to home (/)
                show0message = 'Changes were approved and merged successfully!' if request.POST.get("approve") else 'Changes were discarded successfully!'
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
            'lat': edited_facilitydata.lat,
            'lon': edited_facilitydata.lon,
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
            'ushauri': mhealth_info.Ushauri,
            'nishauri': mhealth_info.Nishauri,
            'c4c': mhealth_info.C4C,
            'mlab': mhealth_info.Mlab,
            'psurvey': mhealth_info.Psurvey,
            'art': mhealth_info.ART_Directory,
            'il_status': il_info.status,
            'webADT_registration': il_info.webADT_registration,
            'webADT_pharmacy': il_info.webADT_pharmacy,
            'three_PM': il_info.three_PM,
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
    return render(request, 'facilities/update_facility.html', {'facilitydata': edited_facilitydata, 'form': form, "title":"Changes Awaiting Approval"})


def delete_facility(request, facility_id):
    # Implementation_type.objects.get(facility_info=facility_id).delete() if Implementation_type.objects.get(facility_info=facility_id) else ""
    # HTS_Info.objects.get(facility_info=facility_id).delete() if HTS_Info.objects.get(facility_info=facility_id) else ""
    # EMR_Info.objects.get(facility_info=facility_id).delete() if EMR_Info.objects.get(facility_info=facility_id) else ""
    # IL_Info.objects.get(facility_info=facility_id).delete() if IL_Info.objects.get(facility_info=facility_id) else ""
    # MHealth_Info.objects.get(facility_info=facility_id).delete() if MHealth_Info.objects.get(facility_info=facility_id) else ""
    Facility_Info.objects.get(pk=facility_id).delete()

    messages.add_message(request, messages.SUCCESS, "Facility successfully deleted!")
    return HttpResponseRedirect('/home')


@login_required(login_url='/login/')
def partners(request):
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

    return render(request, 'facilities/partners_list.html', {'partners_data': partners_data})


def sub_counties(request):
    #sub_counties = Sub_counties.objects.filter(county=county_id)
    #data = serialize("json", sub_counties)
    #return HttpResponse(data, content_type="application/json")
    counties = Counties.objects.all()

    sub_counties_list =[]
    for row in counties:
        sub_counties = Sub_counties.objects.filter(county=row.id).order_by('name')

        subObj = {}
        subObj['county'] = row.id
        subObj['sub_county'] = [{'id': sub.id, 'name': sub.name} for sub in sub_counties]

        sub_counties_list.append(subObj)

    return JsonResponse(sub_counties_list, safe=False)


def get_partners_list(request):
    partners = Partners.objects.select_related('agency').all()

    partners_list =[]
    for row in partners:

        partnerObj = {}
        partnerObj['partner'] = row.id
        partnerObj['agency'] = {'id': row.agency.id, 'name': row.agency.name} if row.agency else {}

        partners_list.append(partnerObj)

    return JsonResponse(partners_list, safe=False)


def get_agencies_list(request):
    agencies = SDP_agencies.objects.all()

    agencies_list =[]
    for row in agencies:
        agencyObj = {}
        agencyObj['id'] = row.id
        agencyObj['name'] = row.name

        agencies_list.append(agencyObj)

    return JsonResponse(agencies_list, safe=False)
  
  