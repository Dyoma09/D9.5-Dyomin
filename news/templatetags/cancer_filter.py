from django import template
import re

register = template.Library()

@register.filter
def censor(value):
    bad_words = ['габарит', 'революция', 'факт', 'разгром', 'ретвит']
    
    for word in bad_words:
        if word.lower() in value.lower():
            pattern = r'(?i)(?<=\b\w)' + re.escape(word[1:])
            value = re.sub(pattern, '*' * (len(word) - 1), value)

    return value
