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
        approved_hours_boolean = restaurant.hours_set.filter(approved=True).exists()
        current_approved_hours = ''
        if approved_hours_boolean:
            current_approved_hours = restaurant.hours_set.filter(approved=True).order_by('-created_at')[0]
        return render(request, 'restaurants/details.html', {
            'restaurant': restaurant,
            'approved_hours_boolean': approved_hours_boolean,
            'current_approved_hours': current_approved_hours,
            })
    else:
        restaurant = Restaurant.objects.create(name=request.POST['name'], address=request.POST['address'], google_place_id=request.POST['google_place_id'])
        print(restaurant)
        return render(request, 'restaurants/details.html', {'restaurant': restaurant})

def update_hours(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    hours = restaurant.hours_set.create(hours=request.POST['hours'], approved=False, pending=True, restaurant=restaurant)
    vote = hours.hoursvote_set.create(vote=True, user=request.user, hours=hours)
    approved_hours_boolean = restaurant.hours_set.filter(approved=True).exists()
    current_approved_hours = ''
    if approved_hours_boolean:
        current_approved_hours = restaurant.hours_set.filter(approved=True).order_by('-created_at')[0]
    return render(request, 'restaurants/details.html', {
        'restaurant': restaurant,
        'approved_hours_boolean': approved_hours_boolean,
        'current_approved_hours': current_approved_hours,
        })