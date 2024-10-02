from django.forms import ModelForm
from django.utils.html import strip_tags
from .models import MoodEntry

class MoodEntryForm(ModelForm):

    class Meta:
        #refers to MoodEntry model
        model = MoodEntry
    
        #defining specifiable fields in the form
        fields = ['mood', 'feelings', 'mood_intensity']

    def clean_mood(self):
        mood = self.cleaned_data["mood"]
        return strip_tags(mood)

    def clean_feelings(self):
        feelings = self.cleaned_data["feelings"]
        return strip_tags(feelings)


