from django.forms import ModelForm
from .models import Organisation, Event, Resource

class OrgForm(ModelForm):
    class Meta:
        model = Organisation
        fields = ['description', 'region', 'email', 'website']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date_time', 'price']

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description']
