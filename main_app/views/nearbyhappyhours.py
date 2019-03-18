import urllib.request
import json
import googlemaps
from datetime import datetime
# from django.utils import timezone
# from django.urls import reverse
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

GOOGLE_MAPS_API_KEY = 'AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE'
IP_STACK_API = '5c2404e5cc460bf450a44e309be04b8d'
GMAPS = googlemaps.Client(key='AIzaSyDAI6Sb4jrQMIOG_JqZvHhf4h9QUQQ9fOE')

def happyhour_index(request):
  happyhourresults = Happyhour.objects.all()
  return render(request, 'happyhour/index.html', { 'happyhourresults': happyhourresults })

def happyhour_detail(request, happyhour_id):
  happyhour = Happyhour.objects.get(id=happyhour_id)
  happyhour_form = HappyhourForm()
  return render(request, 'happyhour/detail.html', { 
    'happyhour': happyhour,
    'happyhour_form': happyhour_form
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
    # print(coordinates[0], coordinates[1])
    # nearby_json = _get_nearby_places(coordinates[0], coordinates[1])
    print_results = _display_nearby_places(_get_nearby_places(coordinates[0], coordinates[1]))
    restaurant_list = list(zip(print_results[0], print_results[1], print_results[2]))
    # for n in range(len(print_results[0])):
    #     restaurant_list.extend([print_results[0][n], print_results[1][n]])
    return render(request, 'nearby.html', {
        # '_display_nearby_places': _display_nearby_places,
        # 'nearby_json': nearby_json,
        # 'print_results': print_results,
        # 'restaurant_name': restaurant_name,
        # 'restaurant_address': restaurant_address,
        'restaurant_list': restaurant_list,
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