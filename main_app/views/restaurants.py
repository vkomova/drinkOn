from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from ..models import Restaurant, Menu, MenuVote, Hours, HoursVote

def check_restaurant(request):
    # print(request.POST)
    print(request.POST['google_place_id'])
    if Restaurant.objects.filter(google_place_id=request.POST['google_place_id']).exists():
        print('exists')
        restaurant = Restaurant.objects.get(google_place_id=request.POST['google_place_id'])
        return render(request, 'restaurants/details.html', {'restaurant': restaurant})
    else:
        restaurant = Restaurant.objects.create(name=request.POST['name'], address=request.POST['address'], google_place_id=request.POST['google_place_id'])
        print(restaurant)
        return render(request, 'restaurants/details.html', {'restaurant': restaurant})
