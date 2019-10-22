from django.db import models
from uuid import uuid4

from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    """placeholder"""
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField(blank=True)

class PersonalNote(Note):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
