from django.db import models
import uuid
from datetime import datetime
from django.conf import settings
# Create your models here.


class Counties(models.Model):
    name = models.CharField(max_length=50)


class Sub_counties(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE)


class SDP_agencies(models.Model):
    name = models.CharField(max_length=50)


class Partners(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(SDP_agencies, on_delete=models.CASCADE, default=None, blank=True, null=True)
    #organization_id = models.UUIDField(default=None, blank=True, null=True)


class Organizations(models.Model):
    name = models.CharField(max_length=100)
    organization_id = models.CharField(max_length=100, default=None, blank=True, null=True)
    access_right = models.CharField(max_length=100, default=None, blank=True, null=True)
    org_access_right = models.ForeignKey(Partners, on_delete=models.CASCADE, default=None, blank=True, null=True)


class Organization_stewards(models.Model):
    steward = models.CharField(max_length=100)
    organization = models.ForeignKey(Partners, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    tel_no = models.IntegerField(default=None, blank=True, null=True)


class EMR_type(models.Model):
    type = models.CharField(max_length=100)


class HTS_use_type(models.Model):
    hts_use_name = models.CharField(max_length=100)


class HTS_deployment_type(models.Model):
    deployment = models.CharField(max_length=100)


class Owner(models.Model):
    name = models.CharField(max_length=100)

class EMR_modules(models.Model):
    name = models.CharField(max_length=100)

class IL_modules(models.Model):
    name = models.CharField(max_length=100)


class Master_Facility_List(models.Model):
    current_page = models.IntegerField(default=None, blank=True, null=True)
    current_index = models.IntegerField(default=None, blank=True, null=True)
    mfl_code = models.IntegerField(default=None, blank=True, null=True)
    name = models.CharField(max_length=100)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, default=None)
    sub_county = models.ForeignKey(Sub_counties, on_delete=models.CASCADE, default=None, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, default=None, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None, blank=True, null=True)
    kmhfltest_id = models.UUIDField(default=None, editable=False, blank=True, null=True)


class Facility_Info(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mfl_code = models.IntegerField(default=None, blank=True, null=True)
    name = models.CharField(max_length=100)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, default=None)
    sub_county = models.ForeignKey(Sub_counties, on_delete=models.CASCADE, default=None, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, default=None, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None, blank=True, null=True)
    kmhfltest_id = models.UUIDField(default=None, editable=False, blank=True, null=True)


class Edited_Facility_Info(models.Model):
    # this stores edited facility data awaiting approval. Once approved, it will be deleted
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mfl_code = models.IntegerField(default=None, blank=True, null=True)
    name = models.CharField(max_length=100)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, default=None)
    sub_county = models.ForeignKey(Sub_counties, on_delete=models.CASCADE, default=None, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, default=None, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE)
    date_edited = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # user_edited = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True) #id of who edited
    user_edited_name = models.CharField(max_length=100, default=None)
    user_edited_email = models.CharField(max_length=100, default=None)



class EMR_Info(models.Model):
    type = models.ForeignKey(EMR_type, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, default=None, blank=True, null=True)
    ovc = models.BooleanField(default=False, blank=True, null=True)
    otz = models.BooleanField(default=False, blank=True, null=True)
    prep = models.BooleanField(default=False, blank=True, null=True)
    tb = models.BooleanField(default=False, blank=True, null=True)
    kp = models.BooleanField(default=False, blank=True, null=True)
    mnch = models.BooleanField(default=False, blank=True, null=True)
    lab_manifest = models.BooleanField(default=False, blank=True, null=True)
    for_version = models.CharField(max_length=20, default="original")
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)
    facility_edits = models.ForeignKey(Edited_Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)


class HTS_Info(models.Model):
    # if only two options are available (N/A or active), a Boolean field might be better
    status = models.CharField(max_length=100, default=None, blank=True, null=True)
    hts_use_name = models.ForeignKey(HTS_use_type, on_delete=models.CASCADE, blank=True, null=True)
    deployment = models.ForeignKey(HTS_deployment_type, on_delete=models.CASCADE, blank=True, null=True)
    for_version = models.CharField(max_length=20, default="original")
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)
    facility_edits = models.ForeignKey(Edited_Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)


class IL_Info(models.Model):
    # consider Boolean field
    status = models.CharField(max_length=100, default=None, blank=True, null=True)
    three_PM = models.BooleanField(default=False, blank=True, null=True)
    air = models.BooleanField(default=False, blank=True, null=True)
    Ushauri = models.BooleanField(default=False, blank=True, null=True)
    Mlab = models.BooleanField(default=False, blank=True, null=True)
    webADT_registration = models.BooleanField(default=False, blank=True, null=True)
    webADT_pharmacy = models.BooleanField(default=False, blank=True, null=True)
    for_version = models.CharField(max_length=20, default="original")
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)
    facility_edits = models.ForeignKey(Edited_Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)


class MHealth_Info(models.Model):
    # consider Boolean field
    #status = models.CharField(max_length=100)
    Ushauri = models.BooleanField(default=False, blank=True, null=True)
    C4C = models.BooleanField(default=False, blank=True, null=True)
    Nishauri = models.BooleanField(default=False, blank=True, null=True)
    Mlab = models.BooleanField(default=False, blank=True, null=True)
    ART_Directory = models.BooleanField(default=False, blank=True, null=True)
    Psurvey = models.BooleanField(default=False, blank=True, null=True)
    for_version = models.CharField(max_length=20, default="original")
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)
    facility_edits = models.ForeignKey(Edited_Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)


class Implementation_type(models.Model):
    #type = models.CharField(max_length=100, default=None)
    ct = models.BooleanField(default=False, blank=True, null=True)
    hts = models.BooleanField(default=False, blank=True, null=True)
    il = models.BooleanField(default=False, blank=True, null=True)
    for_version = models.CharField(max_length=20, default="original")
    facility_info = models.ForeignKey(Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)
    facility_edits = models.ForeignKey(Edited_Facility_Info, on_delete=models.CASCADE, default=None, blank=True, null=True)





