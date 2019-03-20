from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from ..models import Restaurant, Menu, MenuVote, Hours, HoursVote

def view_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    approved_hours_boolean = restaurant.hours_set.filter(approved=True).exists()
    current_approved_hours = ''
    pending_hours_collection = restaurant.hours_set.filter(pending=True)
    pending_hours = ''
    if pending_hours_collection.exists():
        pending_hours = pending_hours_collection[0]
        yay_votes =  pending_hours.hoursvote_set.filter(vote=True)
        nay_votes =  pending_hours.hoursvote_set.filter(vote=False)
    else:
        yay_votes =  ''
        nay_votes =  ''
    if approved_hours_boolean:
        current_approved_hours = restaurant.hours_set.filter(approved=True).order_by('-created_at')[0]
    return render(request, 'restaurants/details.html', {
        'restaurant': restaurant,
        'approved_hours_boolean': approved_hours_boolean,
        'current_approved_hours': current_approved_hours,
        'pending_hours': pending_hours,
        'yay_votes': yay_votes,
        'nay_votes': nay_votes,
        })

def check_restaurant(request):
    print(request.POST['google_place_id'])
    if Restaurant.objects.filter(google_place_id=request.POST['google_place_id']).exists():
        print('exists')
        restaurant = Restaurant.objects.get(google_place_id=request.POST['google_place_id'])
        approved_hours_boolean = restaurant.hours_set.filter(approved=True).exists()
        current_approved_hours = ''
        pending_hours_collection = restaurant.hours_set.filter(pending=True)
        pending_hours = ''
        if pending_hours_collection.exists():
            pending_hours = pending_hours_collection[0]
            yay_votes =  pending_hours.hoursvote_set.filter(vote=True)
            nay_votes =  pending_hours.hoursvote_set.filter(vote=False)
        else:
            yay_votes =  ''
            nay_votes =  ''
        if approved_hours_boolean:
            current_approved_hours = restaurant.hours_set.filter(approved=True).order_by('-created_at')[0]
            return redirect('view_restaurant', restaurant_id=restaurant.id)
    else:
        restaurant = Restaurant.objects.create(name=request.POST['name'], address=request.POST['address'], google_place_id=request.POST['google_place_id'])
        print(restaurant)
        return redirect('view_restaurant', restaurant_id=restaurant.id)

def update_hours(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if len(restaurant.hours_set.filter(pending=True)) == 0:
        if restaurant.hours_set.filter(approved=True).exists():
            hours = restaurant.hours_set.create(hours=request.POST['hours'], approved=False, pending=True, restaurant=restaurant)
            hours.hoursvote_set.create(vote=True, hours=hours, user=request.user)
        else: 
            hours = restaurant.hours_set.create(hours=request.POST['hours'], approved=True, pending=False, restaurant=restaurant)
    current_approved_hours = restaurant.hours_set.filter(approved=True).order_by('-created_at')[0]
    pending_hours_collection = restaurant.hours_set.filter(pending=True).order_by('-created_at')
    pending_hours = ''
    if pending_hours_collection.exists():
        pending_hours = pending_hours_collection[0]
        yay_votes =  pending_hours.hoursvote_set.filter(vote=True)
        nay_votes =  pending_hours.hoursvote_set.filter(vote=False)
    else:
        yay_votes =  ''
        nay_votes =  ''
    approved_hours_boolean = True
    return redirect('view_restaurant', restaurant_id=restaurant.id)

def yay_vote(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    pending_hours = restaurant.hours_set.filter(pending=True).order_by('-created_at')[0]
    if pending_hours.hoursvote_set.filter(user=request.user).exists():
        pass
    else:
        pending_hours.hoursvote_set.create(vote=True, user=request.user)
    yay_votes =  pending_hours.hoursvote_set.filter(vote=True)
    if len(yay_votes) >= 3:
        pending_hours.pending = False
        pending_hours.approved = True
        pending_hours.save()
    return redirect('view_restaurant', restaurant_id=restaurant.id)

def nay_vote(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    pending_hours = restaurant.hours_set.filter(pending=True).order_by('-created_at')[0]
    if pending_hours.hoursvote_set.filter(user=request.user).exists():
        pass
    else:
        pending_hours.hoursvote_set.create(vote=False, user=request.user)
    nay_votes = pending_hours.hoursvote_set.filter(vote=False)
    if len(nay_votes) >= 3:
        pending_hours.pending = False
        pending_hours.approved = False
        pending_hours.save()
    return redirect('view_restaurant', restaurant_id=restaurant.id)