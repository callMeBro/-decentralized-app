from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Topic, CustomUser
from .forms import RoomForm 
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from django.http import HttpResponse

 
def loginP(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, 'base/login_register.html')  # Early return to prevent further processing
        
        user = authenticate(request, email=email, password=password)  # Authenticate the user     
        
        if user is not None:
            login(request, user)                #creates session in the database 
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
            
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutU(request):
    logout(request)
    return redirect('home')



    
 
 
 
def home(request):
    # get q and add condition for if its none else prin empty string 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # use Qlookup method to get the topics
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q) |
                                Q(host__name__icontains=q)
                                )             #get all topics from 
      
     
    # allrooms = Room.objects.all()
    topics = Topic.objects.all()                # get all topics 
    room_count = rooms.count()
    context = {"rooms" : rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)         #Matches /home/

def room(request, pk):
#   get specific room by unique value
    room = Room.objects.get(id=pk)
    context = {'room': room}        
    return render(request, 'base/room.html', context)         #Matches /home/room

def readmore(request):
    context={}
    return render(request, 'base/readmore.html', context)


def createRoom(request):
    form = RoomForm()
    # if request is post
    if request.method == 'POST':
    # get request data
        form = RoomForm(request.POST)
    # if form is vaild save and redirect home
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(request.POST, instance=room)
  
    context={"form":form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj":room})

