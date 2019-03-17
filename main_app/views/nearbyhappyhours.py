import urllib.request
import json
import googlemaps
from datetime import datetime
from django.utils import timezone
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

GOOGLE_MAPS_API_KEY = 'AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE'
IP_STACK_API = '5c2404e5cc460bf450a44e309be04b8d'
GMAPS = googlemaps.Client(key='AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE')

def nearby(request):
    coordinates = _get_location()
    print(coordinates[0], coordinates[1])
    nearby_json = _get_nearby_places(coordinates[0], coordinates[1])
    print_results = _display_nearby_places(nearby_json)
    restaurant_name = print_results[0]
    restaurant_address = print_results[1]
    return render(request, 'nearby.html', {
        # '_display_nearby_places': _display_nearby_places,
        # 'nearby_json': nearby_json,
        'print_results': print_results,
        'restaurant_name': restaurant_name,
        'restaurant_address': restaurant_address,
    })

# Old code
# def nearby(request):
#     coordinates = _get_location()
#     print(coordinates[0], coordinates[1])
#     nearby_json = _get_nearby_places(coordinates[0], coordinates[1])
#     print_results = _display_nearby_places(nearby_json)
#     print(print_results)
#     return render(request, 'nearby.html', {
#         # '_display_nearby_places': _display_nearby_places,
#         # 'nearby_json': nearby_json,
#         'print_results': print_results
#     })

def _get_location():
    f = urllib.request.urlopen('http://api.ipstack.com/check?access_key=' + IP_STACK_API)
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    location_latitude = location['latitude']
    location_longitude = location['longitude']
    return location_latitude, location_longitude

def _get_nearby_places(location_latitude, location_longitude):
    coordinates = (location_latitude, location_longitude)
    return GMAPS.places_nearby(
        location=coordinates,
        # rank_by='distance',
        type='restaurant',
        radius=5000
    )

def _display_nearby_places(nearby_json):
    resultsname = []
    resultsaddress =[]
    for result in nearby_json['results']:
        resultsname.append(result['name']),
        resultsaddress.append(result['vicinity'])
    return resultsname, resultsaddress