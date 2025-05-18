from django.urls import path
from . import views

urlpatterns = [ 
    path('login',views.loginForm , name='login'),
    path('signup',views.signupForm , name='signup'),
    path('logout',views.LogoutForm , name='logout'),
    path('' , views.Home , name = 'home'),
    path('rooms/<str:pk>' , views.room , name ='room' ),
    path('room-form/' , views.createRoom , name='room-form'),
    path('update-room/<str:pk>' , views.updateRoom , name='update-room'),
    path('delete-room/<str:pk>' , views.deleteRoom , name='delete-room'),
    path('delete-message/<str:pk>' , views.deleteMessage , name='delete-message'),
    path('profile/<str:pk>' , views.Profile , name='profile'),
    path('edit-profile' , views.EditProfile , name='edit-profile'),
    path('topics' , views.TopicsName , name='topics'),
    path('activities' , views.activitiesMessages , name='activities'),
]