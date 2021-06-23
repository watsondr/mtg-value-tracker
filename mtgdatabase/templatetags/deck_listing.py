from django.template import Library

register = Library()

"""
https://stackoverflow.com/questions/17178525/django-how-to-include-a-view-from-within-a-template
"""

def return_template(item):
    template = 'null'
    
    context = {
    
    }
    
    return_to_string = 1
    
    return return_to_string(template, context)
