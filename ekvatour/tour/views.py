import json
import operator
from datetime import datetime ,timedelta
from functools import reduce

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic, View
from .models import CountryModel, TourModel, CityModel, TourOptionModel


class CountryListView(generic.ListView):
    model = CountryModel
    template_name = 'tour/country_list.html'
    context_object_name = 'country_list'


class CountryDetailView(generic.DetailView):
    model = CountryModel
    template_name = 'tour/country_detail.html'
    context_object_name = "country"


class TourSearchView(View):
    template_name = 'tour/online.html'

    def get(self, request):
        first_country = CountryModel.objects.first()
        cities = first_country.cities.all()
        return render(request, self.template_name, {"cities": cities})


def get_updated_country(request):
    if request.is_ajax and request.method == "GET":
        country = request.GET.get("country", None)
        if country is not None:
            qs_city = (CityModel.objects.filter(country__name=country)
                       .values('id', 'name'))
            city_data = json.dumps(list(qs_city))
            return JsonResponse(data=city_data, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=True)


def filter_tours(request):
    if request.is_ajax and request.method == "POST":
        country = request.POST.get("country")
        tour_type = request.POST.get("tour_type")
        city_list = request.POST.getlist("city_list[]")
        options_list = request.POST.getlist("options_list[]")
        nutrition_list = request.POST.getlist("nutrition_list[]")
        categories_list = request.POST.getlist("categories_list[]")
        departure_date_start = request.POST.get("departure_date_start")
        departure_date_end = request.POST.get("departure_date_end")
        days_min = int( request.POST.get("days_min"))
        days_max = int(request.POST.get("days_max"))
        number_of_adults = request.POST.get("number_of_adults")
        number_of_child = request.POST.get("number_of_child")

        q_list = []

        if len(city_list) > 0:
            q_list.append(Q(city__id__in=city_list))

        else:
            q_list.append(Q(city__country__name=country))

        if len(departure_date_start) > 0:
            datelist = departure_date_start.split('.')
            date_start = datetime(int(datelist[2]), int(datelist[1]), int(datelist[0]))
            q_list.append(Q(departure_date__gte=date_start))
            min = date_start + timedelta(days=days_min)
            q_list.append(Q(arrival_date__gte=min))
            max = date_start + timedelta(days=days_max)
            q_list.append(Q(arrival_date__lte=max))

        if len(departure_date_end) > 0:
            datelist = departure_date_end.split('.')
            date_start = datetime(int(datelist[2]), int(datelist[1]), int(datelist[0]))
            q_list.append(Q(departure_date__lte=date_start))
            min = date_start + timedelta(days=days_min)
            q_list.append(Q(arrival_date__gte=min))
            max = date_start + timedelta(days=days_max)
            q_list.append(Q(arrival_date__lte=max))

        if len(number_of_adults) > 0:
            q_list.append(Q(number_of_adults=number_of_adults))
        if len(number_of_child) > 0:
            q_list.append(Q(number_of_child=number_of_child))

        if len(options_list) > 0:
            q_list.append(Q(tour_options__in=options_list))
        if len(nutrition_list) > 0:
            q_list.append(Q(tour_nutrition__in=nutrition_list))
        if len(categories_list) > 0:
            q_list.append(Q(tour_category__in=categories_list))
        q_list.append(Q(tour_type=tour_type))
        print(q_list)
        tour_query = TourModel.objects.select_related('city').filter(reduce(operator.and_, q_list))

        for tour in tour_query:
            print(tour.city)
        tour_data = serializers.serialize('json', tour_query,
                                          fields=("city", "tour_type", "departure_date", "arrival_date",
                                                  "departure_time", "accommodation_number", "hotel_name",
                                                  "tour_category", "tour_nutrition", "tour_options", "cost"))

        return JsonResponse(tour_data, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=True)
