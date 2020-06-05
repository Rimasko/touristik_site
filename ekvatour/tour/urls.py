from django.urls import path
from django.views.generic import TemplateView
from .views import (CountryDetailView,
                    CountryListView,
                    TourSearchView,
                    get_updated_country,
                    filter_tours)

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('kruiz/', TemplateView.as_view(template_name="kruizi.html"), name='kruiz'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('online/', TourSearchView.as_view(), name='online'),
    path('online/city_by_country/', get_updated_country, name='online_get_city'),
    path('online/filtertours/', filter_tours, name='online_filter_tours'),
    path('country/<slug:slug>', CountryDetailView.as_view(), name='country_detail'),
    path('country/', CountryListView.as_view(), name='country_list')
]