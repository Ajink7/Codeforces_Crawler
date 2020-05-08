from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('CF_Schedule',views.CF_Schedule,name = 'CF_Schedule'),
    path('',views.Contest,name = 'contest'),
    path('ajax_update',views.ajax_update_contests,name = 'ajax_update_contest'),
    path('CC_Schedule',views.CC_Schedule,name = 'CC_Schedule'),
    path('CF_Schedule2',views.cf_scrape2,name = 'CF_Schedule2'),
    path('atcoder_schedule',views.atcoder_scrape,name="atcoder_schedule"),
]
