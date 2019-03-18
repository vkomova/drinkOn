import urllib.request
import json
import googlemaps
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import HappyhourForm
import uuid
import boto3
from ..models import Happyhour, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'happyhourwdi'

GOOGLE_MAPS_API_KEY = 'AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE'
IP_STACK_API = '5c2404e5cc460bf450a44e309be04b8d'
GMAPS = googlemaps.Client(key='AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE')

def nearby(request):
    coordinates = _get_location()
    # print(coordinates[0], coordinates[1])
    # nearby_json = _get_nearby_places(coordinates[0], coordinates[1])
    print_results = _display_nearby_places(_get_nearby_places(coordinates[0], coordinates[1]))
    # restaurant_name = print_results[0]
    # restaurant_address = print_results[1]
    restaurant_list = list(zip(print_results[0], print_results[1], print_results[2]))
    return render(request, 'nearby.html', {
        # '_display_nearby_places': _display_nearby_places,
        # 'nearby_json': nearby_json,
        # 'print_results': print_results,
        # 'restaurant_name': restaurant_name,
        # 'restaurant_address': restaurant_address,
        'restaurant_list': restaurant_list,
    })

class HappyhourCreate(CreateView):
  model = Happyhour
  fields = '__all__'
  success_url = '/happyhour/'

class HappyhourUpdate(UpdateView):
  model = Happyhour
  fields = ['name', 'address', 'time_start', 'time_end', 'added']
  success_url = '/happyhour/'

# Not sure if we will need a delete form but included just in case
class HappyhourDelete(LoginRequiredMixin, DeleteView):
  model = Happyhour
  success_url = '/happyhour/'

def nearby(request):
  coordinates = _get_location()
  print_results = _display_nearby_places(_get_nearby_places(coordinates[0], coordinates[1]))
  restaurant_list = list(zip(print_results[0], print_results[1], print_results[2]))
  return render(request, 'nearby.html', {
      'restaurant_list': restaurant_list,
  })

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
    resultsid = []
    for result in nearby_json['results']:
        resultsname.append(result['name']),
        resultsaddress.append(result['vicinity'])
        resultsid.append(result['place_id'])
    return resultsname, resultsaddress, resultsid
