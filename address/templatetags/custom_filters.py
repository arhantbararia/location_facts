from django import template

register = template.Library()

@register.filter
def get_element_by_index(value, index):
    try:
        if(index < 0):
            index = len(value) + index
        return value[index]
    except (IndexError, TypeError):
        return None