from django.urls import path
from django.shortcuts import redirect
from .views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: redirect('main:home')),
    path('home', home, name='home'),
    path('create-mood-entry', create_mood_entry, name='create-mood-entry'),
    path('edit-mood-entry/<uuid:id>', edit_mood_entry, name='edit-mood-entry'),
    path('delete-mood-entry/<uuid:id>', delete_mood_entry, name='delete-mood-entry'),
    path('show-xml', show_xml, name='show-xml'),
    path('show-json', show_json, name='show-json'),
    path('show-xml/<uuid:id>', show_xml_by_id, name='show-xml-by-id'),
    path('show-json/<uuid:id>', show_json_by_id, name='show-json-by-id'),
    path('register', register, name='register'),
    path('log-in', log_in, name='log-in'),
    path('log-out', log_out, name='log-out'),
]