import json
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
        return render(request, self.template_name, )


def get_updated_country(request):
    if request.is_ajax and request.method == "GET":
        country = request.GET.get("country", None)
        if country is not None:
            qs_city = (CityModel.objects.filter(country__name=country)
                  .values('id', 'name'))
            city_data = json.dumps(list(qs_city))
            return JsonResponse(data=city_data, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=True)
