from django.db import models
from django.contrib.auth.models import User
import uuid

class MoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    feelings = models.TextField()
    mood_intensity = models.IntegerField()

    #readonly construct property
    is_mood_strong = property(lambda self: self.mood_intensity > 5)

    class Meta:
        verbose_name_plural = 'Mood Entries'
        verbose_name = 'Mood Entry'