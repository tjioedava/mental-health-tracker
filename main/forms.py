from django.forms import ModelForm
from .models import MoodEntry

class MoodEntryForm(ModelForm):

    class Meta:
        #refers to MoodEntry model
        model = MoodEntry
    
        #defining specifiable fields in the form
        fields = ['mood', 'feelings', 'mood_intensity']


