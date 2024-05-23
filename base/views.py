from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm 
# from django.http import HttpResponse

 
def home(request):
    allrooms = Room.objects.all
    
    context = {"rooms" : allrooms}
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
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj":room})

