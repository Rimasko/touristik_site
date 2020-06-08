from django.contrib import admin

from .models import (CountryModel, ImageModel, CityModel,
                     TourOptionModel, TourModel, Review, ReservedTour, News, Feedback)


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
    list_filter = ('is_active', )
    search_fields = ('tour',)
    list_display_links = ('user', 'tour')
    raw_id_fields = ('user', 'tour')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_editable = ('published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'viewed', 'answered')
    list_editable = ('viewed', 'answered')
    search_fields = ('email', 'phone', 'text')
    list_filter = ('viewed', 'answered')
