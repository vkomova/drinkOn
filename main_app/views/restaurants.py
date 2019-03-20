from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
import uuid
import boto3
from ..models import Restaurant, Menu, MenuVote, Hours, HoursVote

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'happyhourwdi'


def view_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    approved_hours_boolean = restaurant.hours_set.filter(approved=True).exists()
    current_approved_hours = ''
    pending_hours_collection = restaurant.hours_set.filter(pending=True).order_by('-created_at')
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

    approved_menu_boolean = restaurant.menu_set.filter(approved=True).exists()
    current_approved_menu = ''
    pending_menu_collection = restaurant.menu_set.filter(pending=True).order_by('-created_at')
    pending_menu = ''
    if pending_menu_collection.exists():
        pending_menu = pending_menu_collection[0]
        menu_yay_votes =  pending_menu.menuvote_set.filter(vote=True)
        menu_nay_votes =  pending_menu.menuvote_set.filter(vote=False)
    else:
        menu_yay_votes =  ''
        menu_nay_votes =  ''
    if approved_menu_boolean:
        current_approved_menu = restaurant.menu_set.filter(approved=True).order_by('-created_at')[0]

    return render(request, 'restaurants/details.html', {
        'restaurant': restaurant,
        'approved_hours_boolean': approved_hours_boolean,
        'current_approved_hours': current_approved_hours,
        'pending_hours': pending_hours,
        'yay_votes': yay_votes,
        'nay_votes': nay_votes,
        'approved_menu_boolean': approved_menu_boolean,
        'current_approved_menu': current_approved_menu,
        'pending_menu': pending_menu,
        'menu_yay_votes': menu_yay_votes,
        'menu_nay_votes': menu_nay_votes,
        })

def check_restaurant(request):
    if Restaurant.objects.filter(google_place_id=request.POST['google_place_id']).exists():
        restaurant = Restaurant.objects.filter(google_place_id=request.POST['google_place_id'])[0]
        return redirect('view_restaurant', restaurant_id=restaurant.id)
    else:
        restaurant = Restaurant.objects.create(name=request.POST['name'], address=request.POST['address'], google_place_id=request.POST['google_place_id'])
        return redirect('view_restaurant', restaurant_id=restaurant.id)

def update_hours(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if len(restaurant.hours_set.filter(pending=True)) == 0:
        if restaurant.hours_set.filter(approved=True).exists():
            hours = restaurant.hours_set.create(hours=request.POST['hours'], approved=False, pending=True, restaurant=restaurant)
            hours.hoursvote_set.create(vote=True, hours=hours, user=request.user)
        else: 
            hours = restaurant.hours_set.create(hours=request.POST['hours'], approved=True, pending=False, restaurant=restaurant)
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

def update_menu(request, restaurant_id):
    menu_file = request.FILES.get('menu_file', None)
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if menu_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + menu_file.name[menu_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(menu_file, BUCKET, key)
            menu_photo_url = f"{S3_BASE_URL}{BUCKET}/{key}"
            if len(restaurant.menu_set.filter(pending=True)) == 0:
                if restaurant.menu_set.filter(approved=True).exists():
                    menu = Menu(menu_photo_url=menu_photo_url, restaurant=restaurant, approved=False, pending=True)
                    menu.save()
                    menu.menuvote_set.create(vote=True, menu=menu, user=request.user)

                else: 
                    menu = Menu(menu_photo_url=menu_photo_url, restaurant=restaurant, approved=True, pending=False)
                    menu.save()
        except:
            print('An error occurred uploading the menu.')
    return redirect('view_restaurant', restaurant_id=restaurant.id)
    # if len(restaurant.menu_set.filter(pending=True)) == 0:
    #     if restaurant.menu_set.filter(approved=True).exists():
    #         menu = restaurant.menu_set.create(menu_photo_url=request.POST['menu_photo_url'], approved=False, pending=True, restaurant=restaurant)
    #         menu.menuvote_set.create(vote=True, menu=menu, user=request.user)
    #     else: 
    #         menu = restaurant.menu_set.create(menu_photo_url=request.POST['menu_photo_url'], approved=True, pending=False, restaurant=restaurant)
