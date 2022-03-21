from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import urllib.parse
import environ

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
    env = environ.Env()
    # reading .env file
    environ.Env.read_env()

    authority= env("AUTHORITY")
    client_id= "dwh.his"
    redirect_uri= request.scheme + "://" + request.META['HTTP_HOST'] +"/signin-oidc"
    response_type= "id_token token"
    scope= "openid profile apiApp"
    post_logout_redirect_uri= request.scheme + "://" + request.META['HTTP_HOST']  #"http://localhost:8000"
    state= generate_nonce()
    nonce= generate_nonce()

    ReturnUrl = '?ReturnUrl=%2FDwhIdentity%2Fconnect%2Fauthorize%2Fcallback'
    client_id = '%3Fclient_id%3D'+client_id
    url = env("LOGIN_URL") + ReturnUrl +  client_id

    auth_token_url = url+'%26redirect_uri%3D'+redirect_uri+'%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520apiApp%26' \
                                                       'state%3D'+state+'%26nonce%3D'+nonce

    return redirect(auth_token_url)


def signin_oidc(request):
    # allows frontend to consume access token and return to backen
    return render(request, 'users/signin_oidc.html')


from django.views.decorators.csrf import csrf_exempt,csrf_protect
@csrf_exempt
def store_tokens(request):
    if request.method == 'POST':
        # print("log_user_in=========>", request.POST.get('scope'), " =================> ",request.POST.get('access_token'))
        # print("id_token=========>", request.POST.get('states'), " =================> ",request.POST.get('id_token'))
        request.session["access_token"] = request.POST.get('access_token')
        request.session["id_token"] = request.POST.get('id_token')
        request.session["state"] = request.POST.get('states')
        request.session["session_state"] = request.POST.get('session_state')

    return JsonResponse({'status': 'success'})

def log_user_in(request):
    env = environ.Env()
    # reading .env file
    environ.Env.read_env()

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + request.session["access_token"]
    url = env("AUTHORITY") + '/connect/userinfo'
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
    env = environ.Env()
    # reading .env file
    environ.Env.read_env()

    redirect_url = 'http://localhost:8000'
    url = env("AUTHORITY") + '/connect/endsession?id_token_hint='+request.session["id_token"]+ \
                               '&post_logout_redirect_uri=' + redirect_url
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





