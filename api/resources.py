from tastypie.resources import ModelResource
from api.models import Note
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication


class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        fields = ['title', 'body']