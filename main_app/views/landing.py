from datetime import datetime
from django.utils import timezone
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Happyhour

# Create your views here.

def happyhour_detail(request, happyhour_id):
  happyhour = happyhour.objects.get(id=happyhour_id)
  return render(request, 'happyhour/detail.html', { 'happyhour': happyhour })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('about')
    else:
      error_message = 'Invalid credentials - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def about(request):
    return render(request, 'about.html')
    # return HttpResponse('about page')

def home(request):
    return render(request, 'home.html')
