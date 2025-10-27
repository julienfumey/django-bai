import django_filters
from .models import Idea, STATUSES


class IdeaFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(label='Status')
    order = django_filters.OrderingFilter(
        fields=(
            ('status', 'status'),
            ('created_at', 'date_creation'),
            ('upvotes', 'upvotes'),
            ('downvotes', 'downvotes'),
        ),
        field_labels={
            'status': 'Status',
            'created_at': 'Date de création',
            'upvotes': 'Votes positifs',
            'downvotes': 'Votes négatifs',
        },
    )

    class Meta:
        model = Idea
        fields = ['status', 'order']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request').user
        super().__init__(*args, **kwargs)

        if not user.is_authenticated:
            self.filters["status"].extra["choices"] = [choice for choice in STATUSES if choice[0] != 0]
        else:
            self.filters["status"].extra["choices"] = STATUSES
