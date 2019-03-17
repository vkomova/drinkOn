from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Happyhour(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField('Address')
    time_start = models.DateTimeField(db_index=True)
    time_end = models.DateTimeField(db_index=True)
    added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'Happyhour_id': self.id})

