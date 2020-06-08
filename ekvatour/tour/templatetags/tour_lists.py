from django import template
from ..models import CountryModel, TourOptionModel, Review, News

register = template.Library()


@register.simple_tag
def country_list():
    return CountryModel.objects


@register.simple_tag
def country_name_list():
    return CountryModel.objects.values('name', 'id')


@register.simple_tag
def all_options_list():
    return TourOptionModel.objects.values('option', 'id')


@register.simple_tag
def last_reviews(count=5):
    return Review.objects.order_by('-created_date')[:count]


@register.simple_tag
def last_news(count=5):
    return News.objects.filter(published=True).order_by('created_date')[:count]


@register.simple_tag
def get_raiting_html(count):
    print(count)
    stars = ''
    for _ in range(count):
        stars += ' <i class="fas fa-star"></i>'

    if 5-count > 0:
        for _ in range(5 - count):
            stars += ' <i class="far fa-star"></i>'
    return stars


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()