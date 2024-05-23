from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Room
from django.forms import ModelForm 


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", 'first_name', 'last_name', 'is_active', 'is_staff')



class RoomForm(ModelForm):
    class Meta:             #set meta data 
        model = Room               #create a from based in room attributes 
        fields = "__all__"              #include all fields 