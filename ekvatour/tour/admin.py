from django.contrib import admin

from .models import (CountryModel, ImageModel, CityModel, TourOptionModel, TourModel)


class ImageModelInline(admin.TabularInline):
    model = ImageModel


@admin.register(CountryModel)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageModelInline, ]


@admin.register(CityModel)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TourOptionModel)
class TourOptionModelAdmin(admin.ModelAdmin):
    list_display = ('option',)


@admin.register(TourModel)
class TourModelAdmin(admin.ModelAdmin):
    list_display = ('tour_type', 'city',)
    filter_horizontal = ('tour_options',)