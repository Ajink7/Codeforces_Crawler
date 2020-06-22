from django.urls import path , re_path , include
from . import views


app_name = 'charts'


urlpatterns = [

    path('',views.charts),
    path('getData/',views.get_data,name="get_data"),
]
