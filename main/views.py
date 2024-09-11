from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .forms import MoodEntryForm
from .models import MoodEntry

def home(request):
    context = {
        'npm': '2306217071',
        'name': 'Dave',
        'class': 'PBP E',
        'mood_entries': MoodEntry.objects.all(),
    }

    return render(request, 'home.html', context)


def create_mood_entry(request):

    form = MoodEntryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('main:home')

    context = {'form': form,}

    return render(request, 'create-mood-entry.html', context)

def show_xml(request):
    mood_entries = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize('xml', mood_entries), content_type='application/xml')

def show_json(request):
    mood_entries = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize('json', mood_entries), content_type='application/json')

def show_xml_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(pk = id)
    return HttpResponse(serializers.serialize('xml', mood_entry), content_type='application/xml')

def show_json_by_id(request, id):
    mood_entry = MoodEntry.objects.filter(pk = id)
    return HttpResponse(serializers.serialize('json', mood_entry), content_type='application/json')