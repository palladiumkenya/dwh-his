# import mysql.connector
# import environ
# from django.core.management import call_command
# import requests
# import json
# import os
# from pathlib import Path
# import uuid
# from facilities.models import *
# from requests.structures import CaseInsensitiveDict
#
#
# def create_db():
#     headers = CaseInsensitiveDict()
#     headers["Accept"] = "application/json"
#     headers["Authorization"] = "Bearer SHadH0bz4KNAzS9c42TesxV4u4ywHh"
#     url = 'http://api.kmhfltest.health.go.ke/api/facilities/facilities/?format=json'
#     response = requests.get(url, headers=headers)
#
#     data = json.loads(response.content)
#     print(data['results'][1]['code'])
#
#
#     lat_long = data['results'][1]["lat_long"] if data['results'][1]["lat_long"] else [None, None]
#     unique_facility_id = uuid.uuid4()
#     facility = Facility_Info.objects.create(id=unique_facility_id, mfl_code=data['results'][1]['code'],
#                                             name=data['results'][1]['name'],
#                                             county=Counties.objects.get(name=data['results'][1]['county_name']),
#                                             sub_county=Sub_counties.objects.get(name=data['results'][1]['sub_county_name']),
#                                             owner=Owner.objects.get(name=data['results'][1]['owner_type_name']),
#                                             #partner=Partners.objects.get(pk=int(form.cleaned_data['partner'])),
#                                             lat=lat_long[0],
#                                             lon=lat_long[1],
#                                             kmhfltest_id=data['results'][1]["id"]
#                                             ).save()
#
#     # save Implementation info
#     implementation_info = Implementation_type(ct=None, hts=None, il=None,
#                                               for_version="original",
#                                               facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
#
#     # save HTS info
#     hts_info = HTS_Info(hts_use_name=None, status=None, deployment=None,
#                         for_version="original",
#                         facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
#
#     # save EMR info
#     emr_info = EMR_Info(type=None, status=None, ovc=None, otz=None, prep=None,
#                         tb=None, kp=None, mnch=None, lab_manifest=None,
#                         for_version="original",
#                         facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
#
#     # save IL info
#     il_info = IL_Info(webADT_registration=None, webADT_pharmacy=None, status=None, three_PM=None,
#                       for_version="original",
#                       facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
#
#     # save MHealth info
#     mhealth_info = MHealth_Info(Ushauri=None, C4C=None,
#                                 Nishauri=None, ART_Directory=None,
#                                 Psurvey=None, Mlab=None,
#                                 for_version="original",
#                                 facility_info=Facility_Info.objects.get(pk=unique_facility_id)).save()
#
#
#     '''env = environ.Env()
#     # reading .env file
#     environ.Env.read_env()
#
#     dataBase = mysql.connector.connect(
#         host="localhost",
#         user=env("DATABASE_USER"),
#         passwd=env("DATABASE_PASSWORD")
#     )
#
#     # preparing a cursor object
#     cursorObject = dataBase.cursor()
#
#
#     # drop if exists database
#     cursorObject.execute("DROP DATABASE IF EXISTS lets_goooo")
#
#     # creating database
#     cursorObject.execute("CREATE DATABASE IF NOT EXISTS lets_goooo")
#
#     #call_command("python -Xutf8 manage.py dumpdata -o mydata.json", interactive=False)
#     call_command("migrate", interactive=False)
#     call_command("loaddata newdata.json", interactive=False)
#
#     # # fetch the facility data
#     # response = requests.get('http://ip-api.com/json')
#     # data = json.loads(response.content)
#     #
#     # # save fetched data in the db
#     # cursorObject.execute("USE mfl_interface_db")
#     # add_facility_data = "insert into facilities_ipdata(city, country, lat, lon) value(%s, %s, %s, %s)"
#     # data = (data['city'], data['country'], data['lat'], data['lon'])
#     # cursorObject.execute(add_facility_data, data)
#     #
#     # dataBase.commit()
#
#     cursorObject.close()
#     dataBase.close()'''
#
#     # env = environ.Env()
#     # environ.Env.read_env()
#     #
#     # dataBase = mysql.connector.connect(
#     #     host="localhost",
#     #     user=env("DATABASE_USER"),
#     #     passwd=env("DATABASE_PASSWORD")
#     # )
#     #
#     # # preparing a cursor object
#     # cursorObject = dataBase.cursor()
#     # cursorObject.execute("USE mfl_interface_db")
#     #
#     # f = open(os.path.join(Path(__file__).resolve().parent.parent, "facilities/test/sample.json"), 'r')
#     # data = json.load(f)
#     #
#     # #for i in data['results']:
#     # #    print(data['results'][1]["code"])
#     # code = data['results'][1]['code']
#     # name = data['results'][1]['name']
#     # lon = data['results'][1]['lat_long'][1]
#     # add_facility_data = "insert into facilities_facility_info(id, mfl_code, name, county_id, lon, partner_id, owner_id) value(uuid.uuid4(), %s, %s, %s, %s, %s, %s)"
#     # data = (data['results'][1]["code"], data['results'][1]["name"], 30, data['results'][1]["lat_long"][1],
#     #         1, 1)
#     # cursorObject.execute(add_facility_data, data)
#     # dataBase.commit()
#     #
#     # f.close()
#     #
#     # cursorObject.close()
#     # dataBase.close()
#
#     return 0