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

class Room_DB(models.Model):
    """db of one instance of generator"""
    id = models.CharField(primary_key=True, max_length = 20)
    coords = models.CharField(max_length = 20)
    description = models.CharField(max_length=500)
    x = models.IntegerField()
    y = models.IntegerField()
    floor = models.IntegerField()
    n_to = models.CharField(max_length = 20,null=True)
    s_to = models.CharField(max_length = 20,null=True)
    e_to = models.CharField(max_length = 20,null=True)
    w_to = models.CharField(max_length = 20,null=True)
    u_to = models.CharField(max_length = 20,null=True)
    d_to = models.CharField(max_length = 20,null=True)
    region = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)


    



