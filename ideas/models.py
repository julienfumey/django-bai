from django.db import models

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

    def __str__(self):
        return self.title

    def upvote(self):
        self.upvotes += 1
        self.save()

    def downvote(self):
        self.downvotes += 1
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

    def __str__(self):
        return f'Comment on {self.idea.title} by {self.created_at}'
