from django.contrib import admin
from django.urls import path, include
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_soft.urls')),
    path('home/', include('base.urls'))         #urls that matches 'home/' string should be taking of by the 'base.url' 
    # path('')
]
