from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.sites.models import Site


def send_mail_signalement(object, reason, commentaire):

    type_object = object.__class__.__name__
    print(type_object)
    context = {
        'object': object,
        'reason': reason,
        'commentaire': commentaire,
    }

    if type_object == 'Idea':
        context['type_object'] = "l'idée"
        context['content'] = object.description
    elif type_object == 'Comment':
        context['type_object'] = 'le commentaire'
        context['content'] = object.content

    mailcontent = render_to_string('ideas/email/email_signalement.txt', context)  # plaintext.render(d)

    send_mail(
        subject="[BaI] Signalement",
        message=mailcontent,
        from_email=settings.FROM_MAIL,
        recipient_list=settings.REVIEWER_MAILS,
        fail_silently=False,
    )


def send_mail_new_idea(idea):
    context = {
        'idea': idea,
        'url': f"https://{Site.objects.get_current().domain}{reverse_lazy('LoginUser')}",
    }

    mailcontent = render_to_string('ideas/email/email_new_idea.txt', context)

    send_mail(
        subject="[BaI] Nouvelle idée soumise",
        message=mailcontent,
        from_email=settings.FROM_MAIL,
        recipient_list=settings.REVIEWER_MAILS,
        fail_silently=False,
    )
