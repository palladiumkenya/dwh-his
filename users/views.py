from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms.users.forms import *


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm (request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm ()

    context = {'form': form}
    return render(request, 'users/register.html', context)