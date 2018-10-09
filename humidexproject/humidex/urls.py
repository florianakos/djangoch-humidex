# chat/urls.py
from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
	url(r'^humidex/(?P<room_name>[^/]+)/$', views.room, name='room'),
    
    url(r'^humidex/', views.index, name='index'),

    path('', views.redirect_to_main, name="redirect_to_main"),

    
    
]