from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


from . import models
from . import forms
from .filters import IdeaFilter


# Create your views here.
class IdeaListView(ListView):
    model = models.Idea
    # queryset = models.Idea.objects.filter(status__in=[1,2]).order_by('-created_at')
    filterset_class = IdeaFilter
    template_name = 'ideas/home.html'
    form_class = forms.ReportForm
    ordering = ['-created_at']
    # paginate_by = 9

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = models.Idea.objects.all()
        else:
            qs = models.Idea.objects.filter(status__in=[1, 2])

        self.filterset = IdeaFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["filter"] = self.filterset
        if self.request.user:
            context["comments_to_moderate"] = models.Comment.objects.filter(status=0)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            commentaire = form.cleaned_data['comment']
            type_ = form.cleaned_data['type_']
            id_ = form.cleaned_data['id_']
            if type_ == 'idea':
                idea = models.Idea.objects.get(pk=id_)
                idea.signaler(reason, commentaire)
            elif type_ == 'comment':
                comment = models.Comment.objects.get(pk=id_)
                comment.signaler(reason, commentaire)
            return redirect(self.request.path)
        else:
            print(form.errors)
        return self.get(self, request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("ideas/idea_list.html", context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)


def idea_upvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.upvote()
    return JsonResponse({"upvote": idea.upvotes})


def idea_downvote(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.downvote()
    return JsonResponse({"downvote": idea.downvotes})


def comment_upvote(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment.upvote()
    return JsonResponse({"upvote": comment.upvotes})


def comment_downvote(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment.downvote()
    return JsonResponse({"downvote": comment.downvotes})


class IdeaDetailView(DetailView):
    model = models.Idea
    template_name = 'ideas/idea_detail.html'
    context_object_name = "idea"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = forms.CommentForm()
        context["report_form"] = forms.ReportForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # récupérer l'article

        if "comment_submit" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                comment = models.Comment(idea=self.object, content=comment_form.cleaned_data['content'])

                if 'answer_to_id' in request.POST:
                    answer_to = models.Comment.objects.get(pk=comment_form.cleaned_data['answer_to_id'])
                    comment.answer_to = answer_to

                comment.save()
                return redirect('idea_detail', pk=self.object.pk)

        if "report_submit" in request.POST:
            report_form = forms.ReportForm(request.POST)
            if report_form.is_valid():
                reason = report_form.cleaned_data['reason']
                commentaire = report_form.cleaned_data['comment']
                type_ = report_form.cleaned_data['type_']
                id_ = report_form.cleaned_data['id_']
                if type_ == 'idea':
                    print(f"toto {id_}")
                    idea = models.Idea.objects.get(pk=id_)
                    idea.signaler(reason, commentaire)
                elif type_ == 'comment':
                    comment = models.Comment.objects.get(pk=id_)
                    comment.signaler(reason, commentaire)
                return redirect(self.request.path)

        return self.get(self, request, *args, **kwargs)
        # answer_form = self.get_form()


@login_required
def publishIdea(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.publish()
    return redirect('idea_detail', pk=pk)

@login_required
def deleteIdea(request, pk):
    idea = models.Idea.objects.get(pk=pk)
    idea.delete()
    return redirect('home')


class IdeaCreateView(CreateView):
    model = models.Idea
    fields = ['title', 'description']
    template_name = 'ideas/idea_create.html'
    success_url = reverse_lazy('idea_create_success')


class postSuccessView(TemplateView):
    template_name = 'ideas/create_success.html'


class login_view(LoginView):
    template_name = 'ideas/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def approve_comment(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment.publish()
    print("toto")
    return redirect(reverse_lazy('home'))


@login_required
def reject_comment(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment.reject()
    print("titi")
    return redirect(reverse_lazy('home'))


# @staff_member_required
# def admin_home(request):
#    idea_to_be_reviewed = models.Idea.objects.filter(status=0)
#    comment_to_be_reviewed = models.Comment.objects.filter()
#
#    return render(request, 'ideas/dashboard/home.html', locals())
