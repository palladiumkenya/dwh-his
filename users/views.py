from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import urllib.parse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.contrib import messages
import random
from requests.structures import CaseInsensitiveDict
import requests
import json
from .forms.users.forms import *


def register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You are already logged in! Logout to register a new user or to login again.')
        return redirect('index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            #messages.success(request, f'Your account has been created. You can log in now!')
            messages.add_message(request, messages.SUCCESS,
                                 'User account successfully created. You can now login!')

            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def signup(request):
    authority= "https://localhost:5006"
    client_id= "dwh.his"
    redirect_uri= "http%253A%252F%252Flocalhost%253A8000%252Fsignin-oidc"
    response_type= "id_token token"
    scope= "openid profile apiApp"
    post_logout_redirect_uri= "http://localhost:8000"
    state= generate_nonce()
    nonce= generate_nonce()

    ReturnUrl = '?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback'
    client_id = '%3Fclient_id%3D'+client_id
    url = 'https://localhost:5006/Account/Login'+ReturnUrl+client_id

    auth_token_url = url+'%26redirect_uri%3D'+redirect_uri+'%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520apiApp%26' \
                                                       'state%3D'+state+'%26nonce%3D'+nonce

    return redirect(auth_token_url)


def signin_oidc(request):

    print('signin_oidc ===>', request.build_absolute_uri())
    # print('trying ------------>', request.GET.get('access_token'))
    print('trying ------------>', request.GET.get('access_token'))

    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkI4NjgyMjk4RUJEOURCNEMzMDRGMjU1QkI2OUREMkE1IiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2NDY4NjM3NjYsImV4cCI6MTY0Njg2NzM2NiwiaXNzIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwNiIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0OjUwMDYvcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiZHdoLmhpcyIsInN1YiI6IjAyMWZkNzYzLTA2MzUtNDg2Ni1hZmRhLThiZTY1MDJmNTkxOCIsImF1dGhfdGltZSI6MTY0Njg2Mzc2NiwiaWRwIjoibG9jYWwiLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6Iks2NURDVkdHWkpJSzQ2NjdQUFVISlVUT0w1R0Q1NkNFIiwibmFtZSI6Ik1hcnkgS2lsZXdlIiwiZW1haWwiOiJtYXJ5a2lsZXdlQGdtYWlsLmNvbSIsIk9yZ2FuaXphdGlvbklkIjoiZTQwNzhiODEtM2RlMC00M2Y1LTliZDctNTIzY2ZmMTI2OTUwIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWFyeWtpbGV3ZUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfbnVtYmVyIjoiKzI1NDcwMjUxMzcwNCIsInBob25lX251bWJlcl92ZXJpZmllZCI6ZmFsc2UsIkZ1bGxOYW1lIjoiTWFyeSBLaWxld2UiLCJqdGkiOiI5RjM2NDAwNDQ1NURDNERBRTgwM0RBNEY1M0RDQkJENCIsInNpZCI6IkRENEY5MTU0NzQ4MDU1MTlDNjUwMDg3QzAwM0YxNzAyIiwiaWF0IjoxNjQ2ODYzNzY2LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiYXBpQXBwIl0sImFtciI6WyJwd2QiXX0.C9Z9jIG2SUemT0cP6uoM0qF-KQZaswFGj9OFgMK30zxERpikQvO62LxLYoVB95iK40R-_jGXjNyORa-KbhCv0gYtPOVmQsQWScUhcrf3JmXrXGhHal5iFaTX6A1epSssqb2uS8MCc-uThHnDezeOXULbuHzCMlGjTvpeh5pOARdmGLiGNKJB2FZU4m2fyBtj-t0rseQQvdlV71RJljXtUw8hmcaktPNXTKAVkU_W5-gFfZRE3YqEx9wcrskinhkrtDf2oOt-x_lHjetAmaoYxshZAfeky5UhMwdlL7cjHA5P6P3ZoDp1lB8lXAB7UXlhZmvz8P7hOEcONJy1he8QLg"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+token
    url = 'https://localhost:5006/connect/userinfo'
    response = requests.get(url, headers=headers, verify=False)
    print('response ====================>', response.status_code)
    print('GET results ==========>', request.GET)
    # fullname = json.loads(response.content.decode('utf-8'))['FullName']
    # request.session["logged_in_username"] = fullname
    # print(json.loads(response.content.decode('utf-8'))['FullName'])
    return render(request, 'users/signin_oidc.html')


from django.views.decorators.csrf import csrf_exempt,csrf_protect
@csrf_exempt
def store_tokens(request):
    if request.method == 'POST':
        print("log_user_in=========>", request.POST.get('scope'))
        request.session["access_token"] = request.POST.get('access_token')
        request.session["id_token"] = request.POST.get('id_token')
        request.session["state"] = request.POST.get('states')
        request.session["session_state"] = request.POST.get('session_state')

    return JsonResponse({'status': 'success'})

def log_user_in(request):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + request.session["access_token"]
    url = 'https://localhost:5006/connect/userinfo'
    response = requests.get(url, headers=headers, verify=False)
    print('response ====================>', response.status_code)

    fullname = json.loads(response.content.decode('utf-8'))['FullName']
    organization = json.loads(response.content.decode('utf-8'))['OrganizationId']
    email = json.loads(response.content.decode('utf-8'))['email']
    request.session["logged_in_username"] = fullname
    request.session["logged_in_user_org"] = organization
    request.session["logged_in_user_email"] = email
    print(json.loads(response.content.decode('utf-8'))['FullName'])
    print('what is the email',json.loads(response.content.decode('utf-8'))['email'], request.session["logged_in_user_email"])

    return HttpResponseRedirect('/')



def generate_nonce(length=32):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def logout_user(request):
    # headers = CaseInsensitiveDict()
    # headers["Accept"] = "application/json"
    # headers["Authorization"] = "Bearer " + request.session["access_token"]
    url = 'https://localhost:5006/connect/endsession?id_token_hint='+request.session["id_token"]+ \
                               '&post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A8000'
    response = requests.get(url, verify=False)
    print('response ====================>', response.status_code, response.content)

    try:
        del request.session['logged_in_username']
        del request.session["logged_in_user_org"]
        del request.session["logged_in_user_email"]
        del request.session["access_token"]
        del request.session["id_token"]
        del request.session["state"]
        del request.session["session_state"]
    except KeyError:
        pass

    return HttpResponseRedirect(url)





