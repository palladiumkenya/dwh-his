from django import forms
from ...models import *


class Update_Partner_Form(forms.Form):
    partner = forms.CharField(label='SDP', max_length=100)
    agency = forms.CharField(label='SDP Agency', max_length=100)

class Sub_Counties_Form(forms.Form):
    county = forms.ChoiceField(label='County')
    sub_county = forms.CharField(label='Sub County', max_length=100)


class Facility_Data_Form(forms.Form):

    mfl_code = forms.IntegerField(label='MFL Code', required=True)
    name = forms.CharField(label='Facility Name', max_length=100)
    county = forms.ChoiceField(label='County')
    sub_county = forms.ChoiceField(label='Sub County')
    owner = forms.ChoiceField(label='Owner')
    lat = forms.DecimalField(label='Latitude', required=False,)
    lon = forms.DecimalField(label='Longitude', required=False)
    partner = forms.ChoiceField(label='SDP', required=False)
    agency = forms.CharField(label='SDP Agency', max_length=100, required=False)
    CT = forms.BooleanField(label='CT', required=False)
    HTS = forms.BooleanField(label='HTS', required=False)
    KP = forms.BooleanField(label='KP', required=False)
    IL = forms.BooleanField(label='IL', required=False)
    # emr info
    emr_type = forms.ChoiceField(label='EMR', required=False)
    emr_status = forms.ChoiceField(label='EMR Status', required=False,
                                       choices=(('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                                ('Discontinued', 'Discontinued'),('N/A', 'N/A')))
    # hts info
    hts_use = forms.ChoiceField(label='HTS Use', required=False)
    hts_deployment = forms.ChoiceField(label='Deployment', required=False)
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
    mshauri = forms.BooleanField(label='Mshauri', required=False)
    nishauri = forms.BooleanField(label='Nishauri', required=False)
    c4c = forms.BooleanField(label='C4C', required=False)

    def __init__(self, *args, **kwargs):
        super(Facility_Data_Form, self).__init__(*args, **kwargs)
        self.fields['agency'].disabled = True
