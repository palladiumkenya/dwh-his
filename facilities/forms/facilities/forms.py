from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from ...models import *



class Update_Partner_Form(forms.Form):
    partner = forms.CharField(label='SDP', max_length=100)
    agency = forms.CharField(label='SDP Agency', max_length=100)

class Sub_Counties_Form(forms.Form):
    county = forms.ChoiceField(label='County')
    sub_county = forms.ChoiceField(label='Existing Sub Counties for selected county', required=False)
    add_sub_county = forms.CharField(label='Add Sub County', max_length=100)


class Facility_Data_Form(forms.Form):

    mfl_code = forms.IntegerField(label='MFL Code', required=True,
                                  #validators=[MinValueValidator(10000, 'MFL Code can only be a length of 5'),MaxValueValidator(99999, 'MFL Code can only be a length of 5')]
                                  )
    name = forms.CharField(label='Facility Name', max_length=100)
    county = forms.ChoiceField(label='County')
    sub_county = forms.ChoiceField(label='Sub County', widget=forms.Select())
    owner = forms.ChoiceField(label='Owner')
    lat = forms.DecimalField(label='Latitude', required=False,)
    lon = forms.DecimalField(label='Longitude', required=False)
    partner = forms.ChoiceField(label='SDP', required=False)
    agency = forms.CharField(label='SDP Agency', max_length=100, required=False)
    CT = forms.BooleanField(label='CT', required=False)
    HTS = forms.BooleanField(label='HTS', required=False)
    IL = forms.BooleanField(label='IL', required=False)
    # emr info
    emr_type = forms.ChoiceField(label='EMR', required=False)
    emr_status = forms.ChoiceField(label='EMR Status', required=False,
                                       choices=(('',''), ('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                                ('Discontinued', 'Discontinued')))
    # hts info
    hts_use = forms.ChoiceField(label='HTS Use', required=False)
    hts_deployment = forms.ChoiceField(label='Deployment', required=False)
    hts_status = forms.ChoiceField(label='HTS Status', required=False,
                                   choices=(('',''), ('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                            ('Discontinued', 'Discontinued')))
    # il info
    il_status = forms.ChoiceField(label='IL Status', required=False,
                                   choices=(('',''), ('Active','Active'),('Stalled/Inactive', 'Stalled/Inactive'),
                                            ('Discontinued', 'Discontinued')))
    three_PM = forms.BooleanField(label='3PM', required=False)
    webADT_registration =forms.BooleanField(label='WebADT Registration', required=False)
    webADT_pharmacy = forms.BooleanField(label='WebADT Pharmacy', required=False)
    # emr info
    ovc_offered = forms.BooleanField(label='OVC', required=False)
    otz_offered = forms.BooleanField(label='OTZ', required=False)
    prep_offered = forms.BooleanField(label='PrEP', required=False)
    tb_offered = forms.BooleanField(label='TB', required=False)
    mnch_offered = forms.BooleanField(label='MNCH', required=False)
    kp_offered = forms.BooleanField(label='KP', required=False)
    lab_man_offered = forms.BooleanField(label='Lab Manifest', required=False)
    # mhealth info
    ushauri = forms.BooleanField(label='Ushauri', required=False)
    mlab = forms.BooleanField(label='MLab', required=False)
    nishauri = forms.BooleanField(label='Nishauri', required=False)
    c4c = forms.BooleanField(label='C4C', required=False)
    art = forms.BooleanField(label='ART Directory', required=False)
    psurvey = forms.BooleanField(label='PSurvey', required=False)

    def __init__(self, *args, **kwargs):
        super(Facility_Data_Form, self).__init__(*args, **kwargs)
        self.fields['agency'].disabled = True
