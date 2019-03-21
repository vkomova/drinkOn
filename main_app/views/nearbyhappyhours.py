import urllib.request
import json
import googlemaps
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from ..models import Photo
import os
import requests
from geopy.geocoders import Nominatim

IPSTACKKEY = os.environ['IP_STACK_API']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
GMAPS = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'happyhourwdi'

data = requests.get("http://iatacodes.org/api/v6/cities?api_key=c05152c1-441f-430e-9c6c-54dca70f1427")
res = data.json()['request']

def inputnearby(request):
  return render(request, 'inputnearby.html')

def nearby(request):
  address = request.POST.get('address')
  if address == None:
    address = request.session.get('session_address', 'no_address')
    if address == 'no_address':
      return redirect('/inputnearby/')
  else: 
    request.session['session_address'] = address
    request.session.modified = True
  geolocator = Nominatim(user_agent="drinkon")
  location = geolocator.geocode(address)
  if location == None:
    return redirect('/inputnearby/')
  location_latitude = location.latitude
  location_longitude = location.longitude
  print_results = _display_nearby_places(_get_nearby_places(location_latitude, location_longitude))
  restaurant_list = list(zip(print_results[0], print_results[1], print_results[2]))
  return render(request, 'nearby.html', {
    'restaurant_list': restaurant_list,
  })

def _get_nearby_places(location_latitude, location_longitude):
  coordinates = (location_latitude, location_longitude)
  return GMAPS.places_nearby(
    location=coordinates,
    rank_by='distance',
    type='restaurant',
    # radius=5000
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

def add_photo(request, happyhour_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, happyhour_id=happyhour_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', happyhour_id=happyhour_id)
