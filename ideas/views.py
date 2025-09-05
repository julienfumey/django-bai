from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import models


# Create your views here.
class IdeaListView(ListView):
    model = models.Idea
    template_name = 'ideas/idea_list.html'


def idea_upvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.upvote()
    return JsonResponse({"upvote": idea.upvotes})


def idea_downvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.downvote()
    return JsonResponse({"downvote": idea.downvotes})


class IdeaDetailView(DetailView):
    model = 'ideas.Idea'
    template_name = 'ideas/idea_detail.html'


class IdeaCreateView(CreateView):
    model = models.Idea
    fields = ['title', 'description']
    template_name = 'ideas/idea_create.html'
    success_url = '/'
