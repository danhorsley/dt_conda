from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Note, Room_DB

class NoteType(DjangoObjectType):

    class Meta:
        model = Note

        interfaces = (graphene.relay.Node,)

class Room_DBType(DjangoObjectType):

    class Meta:
        model = Room_DB

        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):

    notes = graphene.List(NoteType)
    rooms = graphene.List(Room_DBType)

    def resolve_notes(self, info):
        return Note.objects.all()

    def resolve_rooms(self, info):
        return Room_DB.objects.all()

schema = graphene.Schema(query=Query)