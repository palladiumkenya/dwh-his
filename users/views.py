from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

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
    config = {
        "authority": "https://localhost:5006",
        "client_id": "dwh.spa",
        "redirect_uri": "http://localhost:3000/#/signin-oidc#",
        "response_type": "id_token token",
        "scope": "openid profile apiApp",
        "post_logout_redirect_uri": "http://localhost:8000",
        "state": generate_nonce(),
        "nonce": generate_nonce()
    }
    authority= "https://localhost:5006"
    client_id= "dwh.spa"
    #redirect_uri= "http%253A%252F%252Flocalhost%253A8000%252Fsignin-oidc%252F"
    redirect_uri= "https%253A%252F%252F16b9-41-80-22-81.ngrok.io"
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
    return HttpResponseRedirect(auth_token_url)


def signup_callback(request):
    config = {
        "authority": "https://localhost:5006",
        "client_id": "dwh.spa",
        "redirect_uri": "http://localhost:3000/#/signin-oidc#",
        "response_type": "id_token token",
        "scope": "openid profile apiApp",
        "post_logout_redirect_uri": "http://localhost:8000",
        "state": generate_nonce(),
        "nonce": generate_nonce()
    }
    client_id = "dwh.spa"
    ReturnUrl = '?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback'
    client_id = '%3Fclient_id%3D' + client_id
    url = 'https://localhost:5006/Account/Login' + ReturnUrl + client_id
    results = requests.get(url, config, verify=False)
    print(results.content)
    return HttpResponse(results.status_code)


def signin_oidc(request):
    if request.method == 'POST':
        print('signin_oidc')

    return JsonResponse({'help': 'im falling hard'})


def generate_nonce(length=32):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)