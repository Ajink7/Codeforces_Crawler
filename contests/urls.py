from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.contest,name = 'contests'),
    path('scrape',views.scrape,name='scrape'),
]
