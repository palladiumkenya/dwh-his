from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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