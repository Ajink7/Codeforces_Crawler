from django.urls import path , re_path , include
from charts import views


app_name = 'charts'


urlpatterns = [

    path('get_profile/',views.get_profile,name='get_profile'),
]
