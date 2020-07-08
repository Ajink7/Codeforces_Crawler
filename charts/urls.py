from django.urls import path , re_path , include
from . import views


app_name = 'charts'


urlpatterns = [

    path('',views.charts),
    path('getData/',views.get_data,name="get_data"),
    path('comparison/',views.comparison),
    path('getComparison/',views.get_Rating , name="get_Rating"),
    path('getGraphs/',views.get_both_user_ratings,name="get_both_user_ratings")
]
