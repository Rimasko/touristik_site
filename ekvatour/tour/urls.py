from django.urls import path
from django.views.generic import TemplateView
from .views import CountryDetailView, CountryListView, TourSearchView, get_updated_country

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('kruiz/', TemplateView.as_view(template_name="kruizi.html"), name='kruiz'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('online/', TourSearchView.as_view(), name='online'),
    path('online/city_by_country/', get_updated_country, name='online_get_city'),
    path('country/<slug:slug>', CountryDetailView.as_view(), name='country_detail'),
    path('country/', CountryListView.as_view(), name='country_list')
]