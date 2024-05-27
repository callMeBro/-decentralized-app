from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Topic, CustomUser, Message
from .forms import RoomForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

 
def loginP(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == "POST":
        email = request.POST.get('email').lower()
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
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutU(request):
    logout(request)
    return redirect('home')

def registerP(request):
    name = 'register'
    form = CustomUserCreationForm(request.POST)                 #save post requestin form 
    # if form is valid process the user 
    if form.is_valid():
        user = form.save(commit=False)
        user.email = user.email.lower()
        user.save()
        login(request, user)
        return redirect('home')

    else: 
        messages.error(request, "An error occured during registration")
        
    return render(request, 'base/login_register.html', {'form':form}) 
 
 
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
    # Get recent messages
    room_messages = Message.objects.filter(room__in=rooms).order_by('-created')[:5]  # Adjust the number to show more/less messages
    
    context = {"rooms" : rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)         #Matches /home/




def room(request, pk):
    # Get specific room by unique value
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  # Get set of messages related to specific room 
    participants = room.participants.all()  # Get all room participants 

    if request.method == 'POST':        
        body = request.POST.get('body')  # Get request body and save in variable 
        if body:
            # Create the message object 
            Message.objects.create(
                user=request.user,  # Set user who sent the message 
                room=room,  # The room where the comment was posted 
                body=body  # The content of the message 
            )
            
            room.participants.add(request.user)  # Add the user to the participants room
            return redirect('room', pk=room.id)
        else:
            error_message = "Please provide a valid comment."
            context = {
                'room': room,
                'room_messages': room_messages,
                'participants': participants,
                'error_message': error_message
            }
            return render(request, 'base/room.html', context)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)  # Matches /home/room


def readmore(request):
    context={}
    return render(request, 'base/readmore.html', context)

def userP(request, pk):
    user = CustomUser.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME)
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


# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(request.POST, instance=room)
  
#     context={"form":form}
#     return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    user = request.user
    if user != room.host:
        return HttpResponse("You are not allowed here")
    
    
    form = CustomUserCreationForm(instance=user)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    
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

@login_required(login_url='/login')

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        # print("room deleted")
        return redirect("home")
        
    return render(request, 'base/delete.html', {'obj': message})  

