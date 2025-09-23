from django.urls import path

from .views import *

urlpatterns = [
    path('', IdeaListView.as_view(), name='home'),
    path('idea/<pk>/view/', IdeaDetailView.as_view(), name='idea_detail'),
    path('idea/<pk>/up', idea_upvote, name="idea_upvote"),
    path('idea/<pk>/down', idea_downvote, name="idea_downvote"),
    path('comment/<pk>/up', comment_upvote, name="comment_upvote"),
    path('comment/<pk>/down', comment_downvote, name="comment_downvote"),
    path('idea/add/', IdeaCreateView.as_view(), name='idea_create'),
]
