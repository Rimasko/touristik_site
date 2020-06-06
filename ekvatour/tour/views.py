import io
import json
import operator
from datetime import datetime, timedelta
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from .models import CountryModel, TourModel, CityModel, ReservedTour, ImageModel, TourOptionModel, Review, News
from .forms import NewsCreateForm


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
        country_name = request.GET.get('country', None)
        tour_type = request.GET.get('tour_type', None)
        days_min = request.GET.get('days_min', None)
        number_of_adults = request.GET.get('number_of_adults', None)
        departure_date_start = request.GET.get("departure_date_start", None)

        first_country = get_object_or_404(CountryModel,
                                          pk=country_name) \
            if country_name is not None else CountryModel.objects.first()
        cities = first_country.cities.all()
        context = {
            "country_pk": first_country.pk,
            "cities": cities,
            "tour_type": tour_type,
            "days_min": days_min,
            "number_of_adults": number_of_adults,
            "departure_date_start": departure_date_start,
        }
        return render(request, self.template_name, context)


class HotTourView(generic.ListView):
    template_name = "tour/hot_tours.html"
    context_object_name = "tour_list"
    paginate_by = 10

    def get_queryset(self):
        if self.request.method == "GET":
            country = self.request.GET.get('country', None)
            if country is not None:
                return TourModel.objects.filter(city__country__id=country, tour_type="H")
            else:
                return TourModel.objects.filter(tour_type="H")


def get_updated_country(request):
    if request.is_ajax and request.method == "GET":
        country = request.GET.get("country", None)
        if country is not None:
            print(country)
            qs_city = (CityModel.objects.filter(country__id=country)
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
        days_min = int(request.POST.get("days_min"))
        days_max = int(request.POST.get("days_max"))
        number_of_adults = request.POST.get("number_of_adults")
        number_of_child = request.POST.get("number_of_child")

        q_list = []

        if len(city_list) > 0:
            q_list.append(Q(city__id__in=city_list))

        else:
            q_list.append(Q(city__country__id=country))

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
        tour_query = TourModel.objects.select_related('city').filter(reduce(operator.and_, q_list))

        tour_data = serializers.serialize('json', tour_query,
                                          fields=("city", "tour_type", "departure_date", "arrival_date",
                                                  "departure_time", "accommodation_number", "hotel_name",
                                                  "tour_category", "tour_nutrition", "tour_options", "cost", "image"))

        return JsonResponse(tour_data, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=True)


class CreateReview(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ('author', 'tour', 'star', 'text')
    template_name = "LK.html"

    def get_success_url(self):
        return reverse('lk')


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/detail_review.html'
    context_object_name = 'review'


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'review/list_review.html'
    context_object_name = 'reviews'
    paginate_by = 5


class NewsListView(generic.ListView):
    queryset = News.objects.filter(published=True)
    template_name = 'news/list_news.html'
    context_object_name = 'news_list'
    paginate_by = 5


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'news/detail_news.html'
    context_object_name = 'news'


class NewsCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'is_staff'
    form_class = NewsCreateForm
    model = News
    template_name = 'news/news_create.html'


class CreateResevedTour(LoginRequiredMixin, generic.View):

    def post(self, request):
        tour_id = request.POST.get("tour", None)
        if tour_id is not None:
            user = request.user;
            tour = get_object_or_404(TourModel, pk=tour_id)
            ReservedTour.objects.get_or_create(tour=tour, user=user)
            return redirect('lk')

        return HttpResponse(status=403)


def init_():
    from django.core.files import File
    import json
    from pprint import pprint
    with open('test_data.json', 'r') as file:
        data = json.load(file)
        flag = File(open('flag.png', 'rb'))
        bg = File(open("bg.png", 'rb'))

        for i in data:
            country = CountryModel(name=i["name"], about=i["about"], slug=i["slug"])
            country.save()
            country.flag.save('flag.png', flag)
            image = ImageModel(country=country)
            image.image.save('bg.png', bg)

            for c in i["cities"]:
                city = CityModel(name=c["name"], country=country)
                city.save()
                for t in list(c["tours"]):
                    tour = TourModel(city=city, tour_type=t["tour_type"], tour_nutrition=t["tour_nutrition"],
                                     tour_category=t["tour_category"], number_of_child=t["number_of_child"],
                                     number_of_adults=t["number_of_adults"], hotel_name=t["hotel_name"],
                                     accommodation_number=t["accommodation_number"], cost=t["cost"])

                    departure_date = datetime.strptime(t["departure_date"].split('+')[0], "%a %b %d %Y %H:%M:%S %Z")
                    arrival_date = datetime.strptime(t["arrival_date"].split('+')[0], "%a %b %d %Y %H:%M:%S %Z")
                    departure_time = datetime.strptime(t["departure_time"].split('+')[0], "%a %b %d %Y %H:%M:%S %Z")

                    tour.departure_time = departure_time.time()
                    tour.departure_date = departure_date
                    tour.arrival_date = arrival_date
                    tour.image.save('img.png', bg)
                    tour.save()
                    for o in t["tour_options"]:
                        op, _ = TourOptionModel.objects.get_or_create(option=o["option"])
                        op.save()
                        tour.tour_options.add(op)
