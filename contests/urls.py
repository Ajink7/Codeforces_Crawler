from django.contrib import admin
from django.urls import path,include
from .views import *
from .scrape_helper import *
urlpatterns = [
    path('',Contest,name = 'contest'),
    path('ajax_update',ajax_update_contests,name = 'ajax_update_contest'),
    path('ajax/data_filter',ajax_filter,name="ajax_filter"),
    path('atcoder_schedule',atcoder_scrape,name="atcoder_schedule"),
    
]
