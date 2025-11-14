from django.urls import path

from .views import *

urlpatterns = [
    path('', IdeaListView.as_view(), name='home'),
    path('idea/<pk>/view/', IdeaDetailView.as_view(), name='idea_detail'),
    path('idea/<pk>/up', idea_upvote, name="idea_upvote"),
    path('idea/<pk>/down', idea_downvote, name="idea_downvote"),
    path('idea/<pk>/publish', publishIdea, name="publish_idea"),
    path('idea/<pk>/delete', deleteIdea, name="poubelle_idea"),
    path('comment/<pk>/up', comment_upvote, name="comment_upvote"),
    path('comment/<pk>/down', comment_downvote, name="comment_downvote"),
    path('comment/<pk>/publish', approve_comment, name="approve_comment"),
    path('comment/<pk>/reject', reject_comment, name="reject_comment"),
    path('idea/add/', IdeaCreateView.as_view(), name='idea_create'),
    path('idea/received', postSuccessView.as_view(), name='idea_create_success'),
    path('login/', login_view.as_view(), name="LoginUser"),
    # path('dashboard/', admin_home, name='admin_home'),  # Admin dashboard
]
