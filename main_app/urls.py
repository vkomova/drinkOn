from django.urls import path, include
from .views import landing, nearbyhappyhours

urlpatterns = [
    path('', landing.home, name='home'),
    path('about/', landing.about, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', landing.signup, name='signup'),
    path('nearby/', nearbyhappyhours.nearby, name='nearby'),
    path('happyhour/<int:happyhour_id>/', landing.happyhour_detail, name='detail'),
]