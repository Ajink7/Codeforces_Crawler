from django.urls import path , re_path , include
from . import views


app_name = 'charts'


urlpatterns = [

    path('',views.charts,name="home"),
    path('getData/',views.get_data,name="get_data"),
    path('getData/ratings',views.get_user_ratings,name="get_user_ratings"),
]
