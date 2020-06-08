import tempfile
from datetime import datetime
import requests
from .models import CountryModel, ImageModel, CityModel, TourModel, TourOptionModel


def init_(filename):
    random_imageUrl = 'https://picsum.photos/800/400'
    from django.core.files import File
    import json
    from pprint import pprint
    with open(filename, 'r') as file:
        data = json.load(file)
        for i in data:
            country = CountryModel(name=i["name"], about=i["about"], slug=i["slug"])
            country.save()
            flag_response = requests.get(f"https://www.countryflags.io/{i['country_code']}/flat/64.png")
            # Create a temporary file
            lf = tempfile.NamedTemporaryFile()

            # Read the streamed image in sections
            for block in flag_response.iter_content(1024 * 8):
                # If no more file then stop
                if not block:
                    break
                # Write image block to temporary file
                lf.write(block)
            country.flag.save('flag.png', File(lf))
            for _ in range(3):
                random_mage = requests.get(random_imageUrl)
                image = ImageModel(country=country)
                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in random_mage.iter_content(1024 * 8):
                    # If no more file then stop
                    if not block:
                        break
                    # Write image block to temporary file
                    lf.write(block)
                image.image.save('bg.png', File(lf))

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
                    random_mage = requests.get(random_imageUrl)
                    lf = tempfile.NamedTemporaryFile()

                    # Read the streamed image in sections
                    for block in random_mage.iter_content(1024 * 8):
                        # If no more file then stop
                        if not block:
                            break
                        # Write image block to temporary file
                        lf.write(block)
                    tour.image.save('img.png', File(lf))
                    tour.save()
                    for o in t["tour_options"]:
                        op, _ = TourOptionModel.objects.get_or_create(option=o["option"])
                        op.save()
                        tour.tour_options.add(op)
