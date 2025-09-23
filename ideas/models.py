from django.db import models
from .utils import send_mail_signalement
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your models here.

STATUSES = [
    (0, 'New'),
    (1, 'Answered'),
]


class Idea(models.Model):
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    upvotes = models.PositiveIntegerField(
        default=0,
    )
    downvotes = models.PositiveIntegerField(
        default=0,
    )
    answer = models.TextField(
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        max_length=20,
        choices=STATUSES,
        default=0,
    )
    signal = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea_detail', args=[str(self.pk)])

    def upvote(self):
        self.upvotes += 1
        self.save()

    def downvote(self):
        self.downvotes += 1
        self.save()

    def signaler(self, reason, commentaire):
        if self.signal == False:
            send_mail_signalement(self, reason, commentaire)
            self.signal = True
            self.save()
        else:
            pass

    @login_required
    def mark_as_answered(self, answer_text):
        self.answer = answer_text
        self.status = 1
        self.save()


class Comment(models.Model):
    idea = models.ForeignKey(
        Idea,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    upvotes = models.PositiveIntegerField(
        default=0,
    )
    downvotes = models.PositiveIntegerField(
        default=0,
    )
    answer_to = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    signal = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'Comment on {self.idea.title} by {self.created_at}'

    def upvote(self):
        self.upvotes += 1
        self.save()

    def downvote(self):
        self.downvotes += 1
        self.save()

    def signaler(self, reason, commentaire):
        if self.signal == False:
            send_mail_signalement(self, reason, commentaire)
            self.signal = True
            self.save()
        else:
            pass
