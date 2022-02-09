from django import forms
from ...models import *


class Update_Partner_Form(forms.Form):
    partner = forms.CharField(label='SDP', max_length=100)
    agency = forms.CharField(label='SDP Agency', max_length=100)

class Sub_Counties_Form(forms.Form):
    county = forms.ChoiceField(label='County',
                               choices=((i.id, i.name) for i in Counties.objects.all().order_by('name')))
    sub_county = forms.CharField(label='Sub County', max_length=100)


class Facility_Data_Form(forms.Form):

    mfl_code = forms.IntegerField(label='MFL Code', required=True)
    name = forms.CharField(label='Facility Name', max_length=100)
    county = forms.ChoiceField(label='County',
                                       choices=((i.id, i.name) for i in Counties.objects.all().order_by('name')))
    sub_county = forms.ChoiceField(label='Sub County',
                                       choices=((i.id, i.name) for i in Sub_counties.objects.all().order_by('name')))
    owner = forms.ChoiceField(label='Owner',
                                       choices=((i.id, i.name) for i in Owner.objects.all()))
    lat = forms.DecimalField(label='Latitude', required=False,)
    lon = forms.DecimalField(label='Longitude', required=False)
    partner = forms.ChoiceField(label='SDP', required=False,
                                       choices=((i.id, i.name) for i in Partners.objects.all()))
    agency = forms.CharField(label='SDP Agency', max_length=100, required=False)
    CT = forms.BooleanField(label='CT', required=False)
    HTS = forms.BooleanField(label='HTS', required=False)
    KP = forms.BooleanField(label='KP', required=False)
    IL = forms.BooleanField(label='IL', required=False)
    # emr info
    emr_type = forms.ChoiceField(label='EMR', required=False,
                                       choices=((i.id, i.type) for i in EMR_type.objects.all()))
    emr_status = forms.ChoiceField(label='EMR Status', required=False,
                                       choices=(('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                                ('Discontinued', 'Discontinued'),('N/A', 'N/A')))
    # hts info
    hts_use = forms.ChoiceField(label='HTS Use', required=False,
                                 choices=((i.id, i.hts_use_name) for i in HTS_use_type.objects.all()))
    hts_deployment = forms.ChoiceField(label='Deployment', required=False,
                                 choices=((i.id, i.deployment) for i in HTS_deployment_type.objects.all()))
    hts_status = forms.ChoiceField(label='HTS Status', required=False,
                                   choices=(('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                            ('Discontinued', 'Discontinued'),('N/A', 'N/A')))
    # il info
    il_status = forms.ChoiceField(label='IL Status', required=False,
                                   choices=(('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                            ('Discontinued', 'Discontinued'),('N/A', 'N/A')))
    registration_ie =forms.ChoiceField(label='Registration I.E', required=False,
                                   choices=(('Yes','Yes'),('No', 'No'),('N/A', 'N/A')), widget=forms.RadioSelect())
    pharmacy_ie = forms.ChoiceField(label='Pharmacy I.E', required=False,
                                   choices=(('Yes','Yes'),('No', 'No'),('N/A', 'N/A')), widget=forms.RadioSelect())
    # emr info
    ovc_offered = forms.ChoiceField(label='OVC', required=False,
                                        choices=(('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')), widget=forms.RadioSelect())
    otz_offered = forms.ChoiceField(label='OTZ',
                                    choices=(('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')), widget=forms.RadioSelect())
    prep_offered = forms.ChoiceField(label='PrEP', required=False,
                                        choices=(('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')), widget=forms.RadioSelect())
    tb_offered = forms.ChoiceField(label='TB', required=False,
                                    choices=(('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')), widget=forms.RadioSelect())
    # mhealth info
    mshauri = forms.BooleanField(label='Ushauri', required=False)
    nishauri = forms.BooleanField(label='Nishauri', required=False)
    c4c = forms.BooleanField(label='Mlab', required=False)

    def __init__(self, *args, **kwargs):
        super(Facility_Data_Form, self).__init__(*args, **kwargs)
        self.fields['agency'].disabled = True
