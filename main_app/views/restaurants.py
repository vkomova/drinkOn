from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from ..models import Restaurant, Menu, MenuVote, Hours, HoursVote

def display_restaurant(request):
    restaurant = Restaurant.objects.find(google_assigned_id=request.google_assigned_id)
    return render(request, f'restaurants/{restaurant.id}/view.html', 'restaurant': restaurant)

class CreateRestaurant(CreateView):
    model = Restaurant
    fields = '__all__'

def check_restaurant(request):
    if Restaurant.objects.filter(google_assigned_id=request.google_assigned_id).exists():
        # restaurant = Restaurant.objects.find(google_assigned_id=request.google_assigned_id)
        # return render(request, f'restaurants/{restaurant.id}/view.html')
        # display restaurant function
        display_restaurant(request)
    else:
        # Restaurant.objects.create(request)
        # create model
        CreateRestaurant.as_view(request)