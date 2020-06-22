from django.urls import path , re_path , include
from solutions import views


app_name = 'charts'


urlpatterns = [

    path('/',views.get_profile,name='get_profile'),
]
