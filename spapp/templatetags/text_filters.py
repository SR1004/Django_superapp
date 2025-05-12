from django import template
register = template.Library()
@register.filter(name='truncate_words')
def truncate_words(value, num_words=10):
    words = value.split()
    return ' '.join(words[:num_words]) + '...' if len(words) > num_words else value
