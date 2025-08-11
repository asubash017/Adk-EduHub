from django import template

register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    """
    Returns True if the user is in the given group.
    Usage in template: {% if user|in_group:"Teachers" %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()
