from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_mail_signalement(object, reason, commentaire):

    type_object = object.__class__.__name__
    context = {
        'object': object,
        'type_object': type_object,
        'reason': reason,
        'commentaire': commentaire,
    }

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
