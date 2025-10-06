from django import template

register = template.Library()


@register.filter(name='get_count')
def get_count(self):
    return len([x for x in self.all() if x.status == 1])
