from django.urls import path
from django.views.generic import TemplateView
from .views import (CountryDetailView,
                    CountryListView,
                    TourSearchView,
                    get_updated_country,
                    filter_tours,
                    CreateResevedTour,
                    CreateReview,
                    ReviewDetailView,
                    ReviewListView,
                    NewsDetailView,
                    NewsListView,
                    NewsCreateView,
                    HotTourView)

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('kruiz/', TemplateView.as_view(template_name="kruizi.html"), name='kruiz'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('online/', TourSearchView.as_view(), name='online'),
    path('hot/', HotTourView.as_view(), name='hot_tours'),
    path('online/city_by_country/', get_updated_country, name='online_get_city'),
    path('online/filtertours/', filter_tours, name='online_filter_tours'),
    path('reserve_tour/', CreateResevedTour.as_view(), name='reserve_tour'),
    path('review/create/', CreateReview.as_view(), name='review_create'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('review/', ReviewListView.as_view(), name='review_list'),
    path('country/<slug:slug>', CountryDetailView.as_view(), name='country_detail'),
    path('country/', CountryListView.as_view(), name='country_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('news_create/', NewsCreateView.as_view(), name='news_create')
]