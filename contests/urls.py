from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [

    path('',views.Contest,name = 'contest'),
    path('ajax_update',views.ajax_update_contests,name = 'ajax_update_contest'),
    path('ajax/data_filter',views.ajax_filter,name="ajax_filter"),
    path('atcoder_schedule',views.atcoder_scrape,name="atcoder_schedule"),
]
