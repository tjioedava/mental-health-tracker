from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from .forms import MoodEntryForm
from .models import MoodEntry

import datetime

@login_required(login_url='/log-in')
def home(request):

    undefined_message = 'Untracked'
    last_log_in = request.COOKIES.get('last_log_in', undefined_message)

    if last_log_in != undefined_message:
        point_index = last_log_in.find('.')
        last_log_in = last_log_in[0: point_index]

    return render(request, 'home.html', {
        'username': request.user.username,
        'npm': '2306217071',
        'class': 'PBP E',
        'last_log_in': last_log_in,
    })

@login_required(login_url='/log-in')
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:home')

    return render(request, 'create-mood-entry.html', {
        'form': form,
    })

@csrf_exempt
@require_http_methods(['POST',])
def create_mood_entry_ajax(request):
    mood = strip_tags(request.POST.get('mood'))
    feelings = strip_tags(request.POST.get('feelings'))
    mood_intensity = request.POST.get('mood-intensity')

    new_mood = MoodEntry(
        user=request.user,
        mood=mood,
        feelings=feelings,
        mood_intensity=mood_intensity,
    )
    new_mood.save()

    return HttpResponse(b'CREATED', status=201)

@login_required(login_url='/log-in')
def edit_mood_entry(request, id):
    mood = MoodEntry.objects.filter(user=request.user, pk=id)
    if len(mood) == 0:
        return HttpResponseBadRequest()
    mood = mood[0]
    form = MoodEntryForm(request.POST or None, instance=mood)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:home')
        messages.error(request, 'Invalid information about mood entry')

    return render(request, 'edit-mood-entry.html', {
        'form': form,
    })

@login_required(login_url='/log-in')
@require_http_methods(['POST',])
def delete_mood_entry(request, id):
    mood = MoodEntry.objects.filter(user=request.user, pk=id)
    if len(mood) == 0:
        return HttpResponseBadRequest()
    mood = mood[0]
    mood.delete()

    return redirect('main:home')

@login_required(login_url='/log-in')
def show_xml(request):
    mood_entries = MoodEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('xml', mood_entries), content_type='application/xml')

@login_required(login_url='/log-in')
def show_json(request):
    mood_entries = MoodEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', mood_entries), content_type='application/json')

@login_required(login_url='/log-in')
def show_xml_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(user=request.user, pk=id)
    return HttpResponse(serializers.serialize('xml', mood_entry), content_type='application/xml')

@login_required(login_url='/log-in')
def show_json_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(user=request.user, pk=id)
    return HttpResponse(serializers.serialize('json', mood_entry), content_type='application/json')

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered')
            return redirect('main:log-in')

    return render(request, 'register.html', {
        'form': form,
    })

def log_in(request):

    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(request.GET.get('next', reverse('main:home')))
            response.set_cookie('last_log_in', str(datetime.datetime.now()), 60 * 60 * 24 * 7) #set for two weeks in parallel of session ID cookie
            return response
        messages.error(request, 'Incorrect credentials')

    else:
        form = AuthenticationForm(request)
    
    return render(request, 'log-in.html', {
        'form': form,
    })
    
@require_http_methods(['POST',])
def log_out(request):
    logout(request)
    response = redirect('main:log-in')
    response.delete_cookie('last_log_in')
    return response
    
