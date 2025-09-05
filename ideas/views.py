from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import models
from . import forms


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


class IdeaDetailView(FormMixin, DetailView):
    model = models.Idea
    template_name = 'ideas/idea_detail.html'
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # récupérer l'article
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = self.object  # lier au modèle principal
            comment.save()
            return redirect('idea_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)


class IdeaCreateView(CreateView):
    model = models.Idea
    fields = ['title', 'description']
    template_name = 'ideas/idea_create.html'
    success_url = '/'
