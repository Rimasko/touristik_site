from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.urls import reverse


class CountryModel(models.Model):
    """ Описание модели страны """
    name = models.CharField("Название", max_length=100, unique=True, blank=False)
    about = RichTextField("О стране", blank=False)
    flag = models.ImageField("Изображение флага", upload_to='country_flags/')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ImageModel(models.Model):
    """ клас картинка для различных списков картинок"""
    image = models.ImageField(upload_to='list_image/', blank=False)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class TourOptionModel(models.Model):
    option = models.CharField("Название опции", max_length=100, unique=True)

    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"

    def __str__(self):
        return self.option


class TourTypeModel(models.Model):
    name = models.CharField("название направления", max_length=150)

    class Meta:
        verbose_name = "Тип тура"
        verbose_name_plural = "Типы туров"

    def __str__(self):
        return self.name


class CityModel(models.Model):
    name = models.CharField("Название города", max_length=150)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, verbose_name="Страна")

    class Meta:
        verbose_name = "Город"
        verbose_name = "Города"

    def __str__(self):
        return self.name


class TourModel(models.Model):
    TOUR_TYPE_CHOICE = (
        ("H", 'Горчий тур'),
        ("O", "Обычный тур")
    )

    TOUR_CATEGORY_CHOICE = (
        ("SC", "SC"),
        ("HV2", "HV2"),
        ("HV1", "HV1"),
        ("5", "5*"),
        ("4", "4*"),
        ("3", "3*"),
    )
    TOUR_NUTRITION_CHOICE = (
        ("AI", "AI"),
        ("BB", "BB"),
        ("FB", "FB"),
        ("HB", "HB"),
        ("RO", "RO")
    )

    city = models.ForeignKey(CityModel, on_delete=models.CASCADE, verbose_name="Город отправления")
    tour_type = models.CharField("Тип тура", choices=TOUR_TYPE_CHOICE, max_length=1)
    departure_date = models.DateField("Дата вылета", auto_now=False)
    arrival_date = models.DateField("Дата прилета", auto_now=False)
    departure_time = models.TimeField("Время вылета", auto_now=False)
    tour_created = models.DateTimeField("Время создания тура", auto_now=True, auto_created=True)
    number_of_adults = models.PositiveSmallIntegerField("Количество взрослых")
    number_of_child = models.PositiveSmallIntegerField("Количество детей")
    tour_category = models.CharField("Категория тура", choices=TOUR_CATEGORY_CHOICE, max_length=3)
    tour_nutrition = models.CharField("Питание", choices=TOUR_NUTRITION_CHOICE, max_length=2)
    tour_options = models.ManyToManyField(TourOptionModel, related_name='tours')
    image = models.ImageField("Изображение тура", upload_to='tour_images/')

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
