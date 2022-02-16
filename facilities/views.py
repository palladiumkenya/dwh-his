from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import uuid
import mysql.connector
from django.contrib.auth.decorators import login_required

from .models import *
from .forms.facilities.forms import *



def index(request):
    #facilitydata = Facilities.objects.select_related('implementation').get(pk=1)
    facilities_info = Facility_Info.objects.prefetch_related('partner')\
                                                        .select_related('county') \
                                                        .select_related('sub_county').all()

    #implementation_info = Implementation_type.objects.select_related('facility_info').all()

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
        dataObj["county"] = row.county
        dataObj["sub_county"] = row.sub_county
        dataObj["owner"] = row.owner.name
        dataObj["lat"] = row.lat if row.lat else ""
        dataObj["lon"] = row.lon if row.lon else ""
        dataObj["partner"] = row.partner.name
        dataObj["agency"] = row.partner.agency.name
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

    #messages.add_message(request, messages.SUCCESS, 'Welcome to DWH-HIS Portal')
    return render(request, 'facilities/facilities_list.html', {'facilitiesdata': facilitiesdata})


@login_required(login_url='/user/login/')
def add_facility_data(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Facility_Data_Form(request.POST)
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))
        form.fields['owner'].choices = ((i.id, i.name) for i in Owner.objects.all())
        form.fields['partner'].choices = ((i.id, i.name) for i in Partners.objects.all())
        form.fields['emr_type'].choices = ((i.id, i.type) for i in EMR_type.objects.all())
        form.fields['hts_use'].choices = ((i.id, i.hts_use_name) for i in HTS_use_type.objects.all())
        form.fields['hts_deployment'].choices = ((i.id, i.deployment) for i in HTS_deployment_type.objects.all())

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
            implementation_info = Implementation_type(ct=form.cleaned_data['CT'],
                                                        hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL'],
                                                      facility_info=Facility_Info.objects.get(pk=unique_facility_id))

            implementation_info.save()

            if form.cleaned_data['HTS'] == True:
                # save HTS info
                hts_info = HTS_Info(hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                    status=form.cleaned_data['hts_status'],
                                      deployment=HTS_deployment_type.objects.get(pk=int(form.cleaned_data['hts_deployment'])),
                                    facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                hts_info.save()
            else:
                # save HTS info
                hts_info = HTS_Info(hts_use_name=None, status=None, deployment=None,
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
                                    facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                emr_info.save()
            else:
                emr_info = EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
                                    tb=None, kp=None, mnch=None, lab_manifest=None,
                                    facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                emr_info.save()

            # save IL info
            if form.cleaned_data['IL'] == True:
                il_info = IL_Info(webADT_registration=form.cleaned_data['webADT_registration'], webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                   status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['three_PM'],
                                   facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                il_info.save()
            else:
                il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
                                  facility_info=Facility_Info.objects.get(pk=unique_facility_id))
                il_info.save()

            # save MHealth info
            mhealth_info = MHealth_Info(Ushauri=form.cleaned_data['ushauri'], C4C=form.cleaned_data['c4c'],
                               Nishauri=form.cleaned_data['nishauri'], ART_Directory=form.cleaned_data['art'],
                                        Psurvey=form.cleaned_data['psurvey'], Mlab=form.cleaned_data['mlab'],
                                        facility_info=Facility_Info.objects.get(pk=unique_facility_id))
            mhealth_info.save()

            # Redirect to home (/)
            messages.add_message(request, messages.SUCCESS, 'Facility was successfully added and can be viewed below!')
            return HttpResponseRedirect('/home')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Facility_Data_Form()
        #form['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))
        form.fields['owner'].choices = ((i.id, i.name) for i in Owner.objects.all())
        form.fields['partner'].choices = ((i.id, i.name) for i in Partners.objects.all())
        form.fields['emr_type'].choices = ((i.id, i.type) for i in EMR_type.objects.all())
        form.fields['hts_use'].choices = ((i.id, i.hts_use_name) for i in HTS_use_type.objects.all())
        form.fields['hts_deployment'].choices = ((i.id, i.deployment) for i in HTS_deployment_type.objects.all())

    return render(request, 'facilities/update_facility.html', {'form': form, "title":"Add Facility"})


@login_required(login_url='/user/login/')
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
        form.fields['county'].choices = ((i.id, i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((i.id, i.name) for i in Sub_counties.objects.all().order_by('name'))
        form.fields['owner'].choices = ((i.id, i.name) for i in Owner.objects.all())
        form.fields['partner'].choices = ((i.id, i.name) for i in Partners.objects.all())
        form.fields['emr_type'].choices = ((i.id, i.type) for i in EMR_type.objects.all())
        form.fields['hts_use'].choices = ((i.id, i.hts_use_name) for i in HTS_use_type.objects.all())
        form.fields['hts_deployment'].choices = ((i.id, i.deployment) for i in HTS_deployment_type.objects.all())

        if form.is_valid():
            # Save the new category to the database.
            Facility_Info.objects.filter(pk=facility_id).update(mfl_code = form.cleaned_data['mfl_code'],
                name = form.cleaned_data['name'],
                county = Counties.objects.get(pk=int(form.cleaned_data['county'])),
                sub_county = Sub_counties.objects.get(pk=int(form.cleaned_data['sub_county'])),
                owner = Owner.objects.get(pk=int(form.cleaned_data['owner'])),
                partner = Partners.objects.get(pk=int(form.cleaned_data['partner'])),
                #facilitydata.agency = facilitydata.partner.agency.name
                lat = form.cleaned_data['lat'],
                lon = form.cleaned_data['lon'],
            )

            Implementation_type.objects.filter(facility_info=facility_id).update(
                ct=form.cleaned_data['CT'], hts=form.cleaned_data['HTS'], il=form.cleaned_data['IL']
            )

            # save HTS info
            if form.cleaned_data['HTS'] == True:
                HTS_Info.objects.filter(facility_info=facility_id).update(
                                    hts_use_name=HTS_use_type.objects.get(pk=int(form.cleaned_data['hts_use'])),
                                    status=form.cleaned_data['hts_status'],
                                    deployment=HTS_deployment_type.objects.get(pk=int(form.cleaned_data['hts_deployment'])))
            else:
                HTS_Info.objects.filter(facility_info=facility_id).update(hts_use_name=None, status=None, deployment=None)

            # save EMR info
            if form.cleaned_data['CT'] == True:
                EMR_Info.objects.filter(facility_info=facility_id).update(type=EMR_type.objects.get(pk=int(form.cleaned_data['emr_type'])),
                                    status=form.cleaned_data['emr_status'],
                                    ovc=form.cleaned_data['ovc_offered'], otz=form.cleaned_data['otz_offered'],
                                    prep=form.cleaned_data['prep_offered'], tb=form.cleaned_data['tb_offered'],
                                    kp=form.cleaned_data['kp_offered'], mnch=form.cleaned_data['mnch_offered'],
                                    lab_manifest=form.cleaned_data['lab_man_offered'])
            else:
                EMR_Info.objects.filter(facility_info=facility_id).update(type=None, status=None, ovc=None, otz=None, prep=None,
                                                        tb=None, kp=None, mnch=None, lab_manifest=None,)

            # save IL info
            if form.cleaned_data['IL'] == True:
                IL_Info.objects.filter(facility_info=facility_id).update(webADT_registration=form.cleaned_data['webADT_registration'],
                                  webADT_pharmacy=form.cleaned_data['webADT_pharmacy'],
                                  status=form.cleaned_data['il_status'], three_PM=form.cleaned_data['three_PM'])
            else:
                IL_Info.objects.filter(facility_info=facility_id).update(webADT_registration=None, webADT_pharmacy=None,
                                                                         status=None, three_PM=None)

            # save MHealth info
            MHealth_Info.objects.filter(facility_info=facility_id).update(Ushauri=form.cleaned_data['ushauri'], C4C=form.cleaned_data['c4c'],
                                        Nishauri=form.cleaned_data['nishauri'], ART_Directory=form.cleaned_data['art'],
                                        Psurvey=form.cleaned_data['psurvey'], Mlab=form.cleaned_data['mlab'])

            # Redirect to home (/)
            messages.add_message(request, messages.SUCCESS, 'Facility was successfully updated. View changes below!')
            return HttpResponseRedirect('/home')
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
            'owner': facilitydata.owner.id,
            'partner': facilitydata.partner.id,
            'agency': facilitydata.partner.agency.name,
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
        form.fields['county'].choices = ((str(i.id), i.name) for i in Counties.objects.all().order_by('name'))
        form.fields['sub_county'].choices = ((str(i.id), i.name) for i in Sub_counties.objects.all().order_by('name'))
        form.fields['owner'].choices = ((str(i.id), i.name) for i in Owner.objects.all())
        form.fields['partner'].choices = ((str(i.id), i.name) for i in Partners.objects.all())
        form.fields['emr_type'].choices = ((str(i.id), i.type) for i in EMR_type.objects.all())
        form.fields['hts_use'].choices = ((str(i.id), i.hts_use_name) for i in HTS_use_type.objects.all())
        form.fields['hts_deployment'].choices = ((str(i.id), i.deployment) for i in HTS_deployment_type.objects.all())

    return render(request, 'facilities/update_facility.html', {'facilitydata': facilitydata, 'form': form, "title":"Update Facility data"})


@login_required(login_url='/user/login/')
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
        partnerObj['agency'] = {'id': row.agency.id, 'name': row.agency.name}

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