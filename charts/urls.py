from django.urls import path , re_path , include
from . import views


app_name = 'charts'


urlpatterns = [

    path('',views.charts,name="home"),
    path('getData/',views.get_data,name="get_data"),
    path('getData/ratings',views.get_user_ratings,name="get_user_ratings"),
    path('comparison/',views.comparison,name="comparison"),
    path('getComparison/',views.get_Rating , name="get_Rating"),
    path('getGraphs/',views.get_both_user_ratings,name="get_both_user_ratings"),
    path('get_rating_comparison/',views.get_comparison,name='get_comparison')
]
