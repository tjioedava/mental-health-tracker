from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MoodEntryForm
from .models import MoodEntry

import datetime

@login_required(login_url='/login-user')
def home(request):
    context = {
        'name': request.user.username,
        'mood_entries': MoodEntry.objects.filter(user = request.user),
        'last_login': request.COOKIES['last_login']
    }

    return render(request, 'home.html', context)

@login_required(login_url='/login-user')
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        mood_entry = form.save(commit = False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:home')

    context = {'form': form,}

    return render(request, 'create-mood-entry.html', context)

@login_required(login_url='/login-user')
def show_xml(request):
    mood_entries = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize('xml', mood_entries), content_type='application/xml')

@login_required(login_url='/login-user')
def show_json(request):
    mood_entries = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize('json', mood_entries), content_type='application/json')

@login_required(login_url='/login-user')
def show_xml_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(pk = id)
    return HttpResponse(serializers.serialize('xml', mood_entry), content_type='application/xml')

@login_required(login_url='/login-user')
def show_json_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(pk = id)
    return HttpResponse(serializers.serialize('json', mood_entry), content_type='application/json')

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered')
            return redirect('main:home')

    return render(request, 'register.html', {
        'form': form,
    })

def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(request.GET.get('next', reverse('main:home')))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        messages.error(request, 'Incorrect username or password')

    else:
        form = AuthenticationForm(request)
    
    return render(request, 'login.html', {
        'form': form,
    })
    
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login-user'))
    response.delete_cookie('last_login')
    return response
        
    
