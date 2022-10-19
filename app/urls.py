from django.urls import path
from . import views
urlpatterns = [ 
    path('createmusictheme/', views.createmusictheme ),
    path('createmusic/', views.createmusic ),
    path('newalarm/', views.newalarm),
    path('findmusic/', views.findmusic),
    path('home/', views.home),
    path('deleterecord/', views.deleterecord),
    path('deleteall/', views.deleteall),
]