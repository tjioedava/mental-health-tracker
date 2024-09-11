from django.urls import path
from django.shortcuts import redirect
from .views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: redirect('main:home')),
    path('home', home, name='home'),
    path('create-mood-entry', create_mood_entry, name='create-mood-entry'),
    path('show-xml', show_xml, name='show-xml'),
    path('show-json', show_json, name='show-json'),
    path('show-xml/<str:id>', show_xml_by_id, name='show-xml-by-id'),
    path('show-json/<str:id>', show_json_by_id, name='show-json-by-id'),
]