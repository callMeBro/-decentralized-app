from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# create new custom user class
class CustomUser(AbstractUser):
    username = None             #set username field to none 
    name = models.CharField(max_length=255, null=True, blank=True)        #Make username field required 
    email = models.EmailField(_("email address"), unique=True)              #make email field unique

    USERNAME_FIELD = "email"                #set username field to email 
    REQUIRED_FIELDS = []

    objects = CustomUserManager()               #specify all objects from class come from customusermanager 

    def __str__(self):
        return self.email
    
class Topic(models.Model):
    name = models.CharField(max_length=200)    
    
    def __str__(self):
       return self.name or self.email               #use name if available, else use email
   
   
# create room model 
class Room(models.Model):
    # host =
    #topic =
    host = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)                      #set up foriegn key with custom user             
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)                        #set up foriegn key with topic 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    class Meta:
        ordering = ['-updated', '-created']              #ensure newest item in db is first 
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()   
    updated = models.DateTimeField(auto_now=True)                   #update everytime timestamp is saved
    created = models.DateTimeField(auto_now_add=True)               #take snapshot when model is created 
    
    class Meta:
     ordering = ['-updated', 'created']
    
    def __str__(self):
     return self.body[0:50]             #truncate body 
    

        
