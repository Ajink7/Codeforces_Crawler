from django.urls import path , re_path , include
from solutions import views


app_name = 'solutions'


urlpatterns = [

    re_path(r'^user_solution/$',views.user_solution,name='user_solution'),

]
