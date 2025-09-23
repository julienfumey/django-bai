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
    form_class = forms.ReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            commentaire = form.cleaned_data['comment']
            type_ = form.cleaned_data['type_']
            id_ = form.cleaned_data['id_']
            if type_ == 'idea':
                print("toto")
                idea = models.Idea.objects.get(pk=id_)
                idea.signaler(reason, commentaire)
            elif type_ == 'comment':
                comment = models.Comment.objects.get(pk=id_)
                comment.signaler(reason, commentaire)
            return redirect(self.request.path)
        else:
            print(form.errors)
        return self.get(self, request, *args, **kwargs)


def idea_upvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.upvote()
    return JsonResponse({"upvote": idea.upvotes})


def idea_downvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.downvote()
    return JsonResponse({"downvote": idea.downvotes})


class IdeaDetailView(DetailView):
    model = models.Idea
    template_name = 'ideas/idea_detail.html'
    context_object_name = "idea"
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # récupérer l'article

        form = self.form_class(request.POST)
        if form.is_valid():
            comment = models.Comment(idea=self.object, content=form.cleaned_data['content'])

            if 'answer_to_id' in form.cleaned_data:
                answer_to = models.Comment.objects.get(pk=form.cleaned_data['answer_to_id'])

                comment.answer_to = answer_to
            comment.save()
            return redirect('idea_detail', pk=self.object.pk)

        return self.get(self, request, *args, **kwargs)
        # answer_form = self.get_form()


class IdeaCreateView(CreateView):
    model = models.Idea
    fields = ['title', 'description']
    template_name = 'ideas/idea_create.html'
    success_url = '/'
