import json

from django import template

register = template.Library()
@register.filter(name="get")
def get(indexable, i):
    return indexable[i]

@register.simple_tag
def image_list_from_string(image_path_str):
    url_list = json.loads(image_path_str.replace("'", '"'))
    return url_list



@register.filter
def rating_stars(rating):
    full_stars = int(rating)
    decimal_part = rating - full_stars

    star_html = ''
    for _ in range(full_stars):
        star_html += '<i class="fa fa-star"></i> '
    if 0.25 <= decimal_part < 0.75:
        star_html += '<i class="fa fa-star-half-alt"></i>'
    elif decimal_part >= 0.75:
        star_html += '<i class="fa fa-star"></i>'
    return star_html

@register.simple_tag
def parallel_for(list1, list2):
    return zip(list1, list2)

@register.filter
def replace(input_st, sub1_sub2):
    sub1, sub2 = sub1_sub2.split(',')
    return input_st.replace(sub1, sub2)
@register.filter
def subtract(value, arg):
    return value - arg

@register.inclusion_tag('pagination.html')
def pagination(page, page_range,current_query_params):
    return {'page': page, 'page_range': page_range, 'current_query_params':current_query_params}

@register.filter(name='contains')
def contains_filter(value, arg):
    return arg in value

@register.filter
def break_after(value, count):
    """Custom template filter to break out of a loop after a certain number of iterations."""
    return value[:count]

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    print(query)
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
