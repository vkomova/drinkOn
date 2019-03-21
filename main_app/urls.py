from django.urls import path, include
from .views import landing, nearbyhappyhours, restaurants

urlpatterns = [
    path('', landing.home, name='home'),
    path('about/', landing.about, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', landing.signup, name='signup'),
    path('inputnearby/', nearbyhappyhours.inputnearby, name='inputnearby'),
    path('nearby/', nearbyhappyhours.nearby, name='nearby'),
    path('restaurants/details', restaurants.check_restaurant, name='restaurant_details'),
    path('restaurants/<int:restaurant_id>/details', restaurants.view_restaurant, name='view_restaurant'),
    path('restaurants/<int:restaurant_id>/update_hours', restaurants.update_hours, name='update_hours'),
    path('restaurants/<int:restaurant_id>/yay_vote', restaurants.yay_vote, name='yay_vote'),
    path('restaurants/<int:restaurant_id>/nay_vote', restaurants.nay_vote, name='nay_vote'),
    path('restaurants/<int:restaurant_id>/update_menu', restaurants.update_menu, name='update_menu'),
]