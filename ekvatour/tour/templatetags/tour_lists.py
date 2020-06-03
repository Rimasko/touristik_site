from django import template
from ..models import CountryModel, TourOptionModel

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