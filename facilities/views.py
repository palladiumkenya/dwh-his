from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import urllib.request, json
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import uuid
import mysql.connector
from .models import *
from .forms.facilities.forms import *
from django.contrib.auth.decorators import login_required


def index(request):
    #facilitydata = Facilities.objects.select_related('implementation').get(pk=1)
    facilities_info = Facility_Info.objects.prefetch_related('partner')\
                                                        .select_related('county') \
                                                        .select_related('sub_county').all()

    implementation_info = Implementation_type.objects.select_related('facility_info').all()

    facilitiesdata = []
    for row in facilities_info:
        implementation_info = Implementation_type.objects.get(facility_info=row.id)
        emr_info = EMR_Info.objects.get(facility_info=row.id)
        hts_info = HTS_Info.objects.get(facility_info=row.id)
        il_info = IL_Info.objects.get(facility_info=row.id)
        mhealth_info = MHealth_Info.objects.get(facility_info=row.id)

        ct = "CT" if implementation_info.ct else ""
        hts = "HTS" if implementation_info.hts else ""
        kp = "KP" if implementation_info.kp else ""
        il = "IL" if implementation_info.il else ""

        implementation = [ct, hts, kp, il]

        dataObj = {}
        dataObj["id"] = row.id
        dataObj["mfl_code"] = row.mfl_code
        dataObj["name"] = row.name
        dataObj["county"] = row.county
        dataObj["sub_county"] = row.sub_county
        dataObj["owner"] = row.owner.name
        dataObj["lat"] = row.lat
        dataObj["lon"] = row.lon
        dataObj["partner"] = row.partner.name
        dataObj["agency"] = row.partner.agency.name
        dataObj["implementation"] = implementation
        dataObj["emr_type"] = emr_info.type.type
        dataObj["emr_status"] = emr_info.status
        dataObj["hts_use"] = hts_info.hts_use_name.hts_use_name
        dataObj["hts_deployment"] = hts_info.deployment.deployment
        dataObj["hts_status"] = hts_info.status
        dataObj["il_status"] = il_info.status
        dataObj["il_registration_ie"] = il_info.registration_ie
        dataObj["il_pharmacy_ie"] = il_info.pharmacy_ie
        dataObj["mhealth_ovc"] = mhealth_info.nishauri

        facilitiesdata.append(dataObj)

    return render(request, 'facilities/facilities_list.html', {'facilitiesdata': facilitiesdata})


@login_required(login_url='/user/login')
def add_facility_data(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        # check whether it's valid:

        if form.is_valid():
            unique_facility_id = uuid.uuid4()
            # Save the new category to the database.
            facility = Facility_Info.objects.create(id=unique_facility_id, mfl_code = form.cleaned_data['mfl_code'],
                name = form.cleaned_data['name'],
                county = Counties.objects.get(pk=int(form.cleaned_data['county'])),
                sub_county = Sub_counties.objects.get(pk=int(form.cleaned_data['sub_county'])),
                owner = Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                partner = Partners.objects.get(pk=int(form.cleaned_data['partner'])),
                #facilitydata.agency = facilitydata.partner.agency.name
                lat = form.cleaned_data['lat'],
                lon = form.cleaned_data['lon']
            )

            facility.save()

            # save Implementation info
            implementation_info = Implementation_type(ct=form.cleaned_data['CT'], kp=form.cleaned_data['KP'],
                                hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                      facility_info=Facility_Info.objects.get(pk=unique_facility_id))

            implementation_info.save()

            # save HTS info
            hts_info = HTS_Info(hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                status=form.cleaned_data['hts_status'],
                                  deployment=HTS_deployment_type.objects.get(pk=int(form.cleaned_data['hts_deployment'])),
                                facility_info=Facility_Info.objects.get(pk=unique_facility_id))
            hts_info.save()

            # save EMR info
            emr_info = EMR_Info(type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                                 status=form.cleaned_data['emr_status'],
                                ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                                prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                                facility_info=Facility_Info.objects.get(pk=unique_facility_id))
            emr_info.save()

            # save IL info
            il_info = IL_Info(registration_ie=form.cleaned_data['registration_ie'], pharmacy_ie=form.cleaned_data['pharmacy_ie'],
                               status=form.cleaned_data['il_status'],
                               facility_info=Facility_Info.objects.get(pk=unique_facility_id))
            il_info.save()

            # save MHealth info
            mhealth_info = MHealth_Info(mshauri=form.cleaned_data['mshauri'], c4c=form.cleaned_data['c4c'],
                               nishauri=form.cleaned_data['nishauri'],
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
            mhealth_info.save()

            # Redirect to home (/)
            return HttpResponseRedirect('/facilities')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Facility_Data_Form()

    return render(request, 'facilities/update_facility.html', {'form': form, "title":"Add Facility"})


@login_required(login_url='/user/login')
def update_facility_data(request, facility_id):
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
        # check whether it's valid:

        if form.is_valid():
            # Save the new category to the database.
            Facility_Info.objects.filter(pk=facility_id).update(mfl_code = form.cleaned_data['mfl_code'],
                name = form.cleaned_data['name'],
                county = form.cleaned_data['county'],
                sub_county = form.cleaned_data['sub_county'],
                owner = int(form.cleaned_data['owner']),
                partner = int(form.cleaned_data['partner']),
                #facilitydata.agency = facilitydata.partner.agency.name
                lat = form.cleaned_data['lat'],
                lon = form.cleaned_data['lon'],
                #emr_type = int(form.cleaned_data['emr_type']),
                #emr_status = int(form.cleaned_data['emr_status']),
                #hts_use_and_deployment = int(form.cleaned_data['hts_use']),
                #facilitydata.deployment = facilitydata.hts_use_and_deployment.deployment)
                #hts_status = int(form.cleaned_data['hts_status']),
                #il_status = int(form.cleaned_data['il_status']),
            )

            Implementation_type.objects.filter(facility_info=facility_id).update(
                ct=form.cleaned_data['CT'],
                hts = form.cleaned_data['HTS'],
                il = form.cleaned_data['KP'],
                kp = form.cleaned_data['IL']
            )

            EMR_Info.objects.filter(facility_info=facility_id).update(
                type=int(form.cleaned_data['emr_type']),
                status=form.cleaned_data['emr_status'],
                ovc=form.cleaned_data['ovc_offered'],
                otz=form.cleaned_data['otz_offered'],
                prep=form.cleaned_data['prep_offered'],
                tb=form.cleaned_data['tb_offered'],
            )

            HTS_Info.objects.filter(facility_info=facility_id).update(
                status=form.cleaned_data['hts_status'],
                hts_use_name=int(form.cleaned_data['hts_use']),
                deployment=int(form.cleaned_data['hts_deployment']),
            )

            IL_Info.objects.filter(facility_info=facility_id).update(
                status=form.cleaned_data['il_status'],
                registration_ie=form.cleaned_data['registration_ie'],
                pharmacy_ie=form.cleaned_data['pharmacy_ie'],
            )

            MHealth_Info.objects.filter(facility_info=facility_id).update(
                nishauri=form.cleaned_data['ovc_offered'],
                mshauri=form.cleaned_data['mshauri'],
                c4c=form.cleaned_data['c4c']
            )

            # Redirect to home (/)
            return HttpResponseRedirect('/facilities')
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
            'owner': facilitydata.owner.name,
            'sdp': facilitydata.partner.name,
            'agency': facilitydata.partner.agency.name,
            'lat': facilitydata.lat,
            'lon': facilitydata.lon,
            'CT': implementation_info.ct,
            'HTS': implementation_info.hts,
            'KP': implementation_info.kp,
            'IL': implementation_info.il,
            'ovc_offered': emr_info.ovc,
            'otz_offered': emr_info.otz,
            'tb_offered': emr_info.tb,
            'prep_offered': emr_info.prep,
            'mshauri': mhealth_info.mshauri,
            'nishauri': mhealth_info.nishauri,
            'c4c': mhealth_info.c4c,
            'il_status': il_info.status,
            'registration_ie': il_info.registration_ie,
            'pharmacy_ie': il_info.pharmacy_ie,
            'emr_type': emr_info.type.type,
            'emr_status': emr_info.status,
            'hts_use': hts_info.hts_use_name,
            'hts_deployment': hts_info.deployment,
            'hts_status': hts_info.status,
        }
        form = Facility_Data_Form(initial=initial_data)

    return render(request, 'facilities/update_facility.html', {'facilitydata': facilitydata, 'form': form, "title":"Update Facility data"})

def partners(request):
    partners_data = Partners.objects.prefetch_related('agency').all()

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
        partnerObj['agency'] = {'id': row.agency.id, 'name': row.agency.name}

        partners_list.append(partnerObj)

    return JsonResponse(partners_list, safe=False)