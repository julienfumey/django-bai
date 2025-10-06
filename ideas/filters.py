import django_filters
from .models import Idea, STATUSES


class IdeaFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(label='Status')

    class Meta:
        model = Idea
        fields = ['status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request').user
        super().__init__(*args, **kwargs)

        if not user.is_authenticated:
            self.filters["status"].extra["choices"] = [choice for choice in STATUSES if choice[0] != 0]
        else:
            self.filters["status"].extra["choices"] = STATUSES
