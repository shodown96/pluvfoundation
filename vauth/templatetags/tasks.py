from django import template
register = template.Library()

@register.filter
def tasks_count(tasks):
    return tasks.filter(verified=False).count()

@register.filter
def filter_tasks(tasks):
    return tasks.filter(verified=False)

@register.filter
def verified(tasks):
    return tasks.filter(verified=True).count()
