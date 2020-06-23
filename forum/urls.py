from django.urls import path,include
from .views import *
app_name = 'forum'
urlpatterns = [
    path('',home,name="home"),
    path('boards/<int:pk>',board_topics,name = 'board_topics'),
    path('boards/<int:pk>/new', new_topic, name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>',topic_posts,name = 'topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply',reply_topic,name = 'reply_topic'),

]
