import googlemaps
from django.conf import settings


class GeoResolver:
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY

    def get_coordinates(self, country, city, street, house_no):
        search_string = ','.join((country, city, '{} {}'.format(street, house_no)))
        gmaps = googlemaps.Client(key=self.api_key)
        location = gmaps.geocode(search_string)
        if location:
            return location[0].get('geometry').get('location')