from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('CF_Schedule',views.CF_Schedule,name = 'CF_Schedule'),
    path('',views.Contest,name = 'contest')
    
]
