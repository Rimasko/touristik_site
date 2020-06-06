from django.contrib import admin
from django.utils.text import slugify

from .models import (CountryModel, ImageModel, CityModel, TourOptionModel, TourModel, Review, ReservedTour, News)


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


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('tour', 'author', 'star')


@admin.register(ReservedTour)
class ReservedTourAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('tour', 'user', 'is_active')
    search_fields = ('tour', )
    list_display_links = ('user', 'tour')
    raw_id_fields = ('user',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_editable = ('published', )
    prepopulated_fields = {'slug': ('title',)}

