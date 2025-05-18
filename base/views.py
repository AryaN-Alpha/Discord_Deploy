from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room , Topic ,Message
from .forms import RoomForm ,UserUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout 
# Create your views here.

def Home(request):    
    q = request.GET.get('q', '')       
    rooms = Room.objects.filter(Q(topic__name__icontains=q)   |  #Q used to add multiple conditinos on filters function like or and and with this we can add filters on multiple conditions 
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))



    return render (request , 'base/Home.html', {'rooms': rooms , 'topic': topic , 'room_count' : room_count ,'room_messages':room_messages }  )



def Profile(request , pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()

    context={'user': user , 'rooms':rooms , 'room_messages' : room_messages , 'topic' : topic}
    return render (request , 'base/profile.html' , context)




def room(request , pk ):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if(request.method == 'POST'):
        message = Message.objects.create (
            host = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room' , pk=room.id)

    return render (request , 'base/room.html' , {'room': room , 'room_messages':room_messages , 'participants':participants  })

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()  # here it creates a form and store it in form
    topics = Topic.objects.all()
    #if request.method=='POST': # request.method returns which type of request is made
        # form = RoomForm(request.POST)   # This stores input fields data into form and store the result in form
        #  if form.is_valid(): # check validity 
        #    room= form.save(commit=False)     # save the form data into database
        #    room.host=request.user
        #    room.save()
        #    return redirect('home') # redirect the page to home page
    if request.method == 'POST':
           
        topic_name = request.POST.get('topics') #cannot directly insert topic in Room table bcz it is string type so we type cast it into Topic object  using get_or_created method bcz topic is Topic foreign key
        topic , created = Topic.objects.get_or_create(name=topic_name) # check if the object is present in Room database if it is it return that specific object from it else it craete a new object and returns it

        Room.objects.create (
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {'form' : form , 'topics':topics}    
    return render (request , 'base/room_form.html' , context)


@login_required(login_url='login')
def updateRoom(request , pk):
    room = Room.objects.get(id=pk)  # get functions is used when we want any specific data | we first fetched the room which we want to update
    form = RoomForm(instance=room)  #instance is previour object of that room | here we find the form which contains previous data 
    print("Heelo  start")
    if request.user != room.host  :
        return HttpResponse('You are not the Correct User')
        
    topics = Topic.objects.all()
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         return redirect ('home')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topics')
        topic ,created = Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form' : form , 'topics':topics , 'room':room}
    return render ( request , 'base/room_form.html' , context) # form.as_p automaticaly fill the attribute with the argument data 

@login_required(login_url='login')
def deleteRoom(request , pk ):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not the Correct User')
        
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    form = {'room':room}
    return render(request , 'base/confirmation_tab.html' , form)
         
def loginForm(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username , password=password)
            if user != None:
                login(request, user)
                return redirect('home')
            else:
                print("Cannot Login User" , user)
        except:
            print("Invalid User Credentials")
    
    context = {'page' : page}
    return render (request , 'base/LoginPage.html' , context)

def signupForm(request):
    page ='signup'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Something went Wrong")    


    context = {'page':page , 'form': form}
    return render (request , 'base/LoginPage.html' , context)

def LogoutForm(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deleteMessage(request , pk ):
    message = Message.objects.get(id=pk)
    
    if request.user != message.host:
        return HttpResponse('You are not the Correct User')
        
    
    if request.method=='POST':
        message.delete()
        return redirect('room' , message.room.id)
    form = {'room':message}
    return render(request , 'base/confirmation_tab.html' , form)

def EditProfile (request):
    form = UserUpdateForm(instance=request.user)
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile' , pk=request.user.id)

    
    return render (request , 'base/edit-user.html' , {'form':form})

def TopicsName(request):
    topics = Topic.objects.all()
    
    if request.method =='POST':
        topics = Topic.objects.filter(name__icontains=request.POST.get('topicname'))
    context= {'topics': topics , }
    return render(request , 'base/topics.html' , context)

def activitiesMessages (request):
    messages = Message.objects.all()

    return render(request , 'base/activity.html' , {'messages':messages})