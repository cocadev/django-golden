from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import CustomUserCreationForm
from .models import User, Dealer, Client
from django.urls import reverse
from management.models import Employee


def login(request):
    c = {}
    c.update(request)
    return render(request, 'dashboard/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(request=request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if isinstance(user, User) or isinstance(user, Dealer) or isinstance(user, Employee):
            return HttpResponseRedirect('/accounts/')
        else:
            return HttpResponseRedirect(reverse('secure.public.profile'))
    else:
        return HttpResponseRedirect('/accounts/login/?error=login')


def public_auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(request=request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('secure.public.profile'))
    else:
        return HttpResponseRedirect('/manage/login/?error=login')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/')


def public_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')

    else:
        form = CustomUserCreationForm()
    args = {}
    args['form'] = form

    return render(request, 'dashboard/register.html', args)


def register_success(request):
    return render(request, 'dashboard/register_success.html')
