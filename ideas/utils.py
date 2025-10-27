from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


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
        subject='Votre offre d\'emploi',
        message=mailcontent,
        from_email=settings.REPORT_EMAIL,
        recipient_list=[
            settings.REPORT_EMAIL,
        ],
        fail_silently=False,
    )
