from django.forms import ModelForm
from .models import Happyhour

class HappyhourForm(ModelForm):
  class Meta:
    model = Happyhour
    fields = ['name', 'address', 'time_start', 'time_end', 'added']