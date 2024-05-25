from django.forms import ModelForm 
from .models import Room


class RoomForm(ModelForm):
    class Mata:             #set meta data 
        models = Room               #create a from based in room attributes 
        fields = "__all__"              #include all fields 