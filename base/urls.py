from django.urls import path
from . import views 


urlpatterns = [
    path('login/', views.loginP, name ='login'), 
    path('logout/', views.logoutU, name ='logout'), 
    path('register/', views.registerP, name ='register'), 
    path('profile/<str:pk>/', views.userP, name='user-profile'),
    
    
    
    path('', views.home, name ='home'), 
    path('room/<str:pk>', views.room, name= 'room'),
    path('readmore/', views.readmore, name= 'readmore'),
    
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),  # Changed <str:pk> to <int:pk> if pk should be an integer
    
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"), 
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room")
    
    
    
]