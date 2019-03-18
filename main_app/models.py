from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

TIME_CHOICES = (('00:00 AM', '00:00 AM'),
                ('00:30 AM', '00:30 AM'),
                ('01:00 AM', '01:00 AM'),
                ('01:30 AM', '01:30 AM'),
                ('02:00 AM', '02:00 AM'),
                ('02:30 AM', '02:30 AM'),
                ('03:00 AM', '03:00 AM'),
                ('03:30 AM', '03:30 AM'),
                ('04:00 AM', '04:00 AM'),
                ('04:30 AM', '04:30 AM'),
                ('05:00 AM', '05:00 AM'),
                ('05:30 AM', '05:30 AM'),
                ('06:00 AM', '06:00 AM'),
                ('06:30 AM', '06:30 AM'),
                ('07:00 AM', '07:00 AM'),
                ('07:30 AM', '07:30 AM'),
                ('08:00 AM', '08:00 AM'),
                ('08:30 AM', '08:30 AM'),
                ('09:00 AM', '09:00 AM'),
                ('09:30 AM', '09:30 AM'),
                ('10:00 AM', '10:00 AM'),
                ('10:30 AM', '10:30 AM'),
                ('11:00 AM', '11:00 AM'),
                ('11:30 AM', '11:30 AM'),
                ('12:00 PM', '12:00 PM'),
                ('12:30 PM', '12:30 PM'),
                ('01:00 PM', '01:00 PM'),
                ('01:30 PM', '01:30 PM'),
                ('02:00 PM', '02:00 PM'),
                ('02:30 PM', '02:30 PM'),
                ('03:00 PM', '03:00 PM'),
                ('03:30 PM', '03:30 PM'),
                ('04:00 PM', '04:00 PM'),
                ('04:30 PM', '04:30 PM'),
                ('05:00 PM', '05:00 PM'),
                ('05:30 PM', '05:30 PM'),
                ('06:00 PM', '06:00 PM'),
                ('06:30 PM', '06:30 PM'),
                ('07:00 PM', '07:00 PM'),
                ('07:30 PM', '07:30 PM'),
                ('08:00 PM', '08:00 PM'),
                ('08:30 PM', '08:30 PM'),
                ('09:00 PM', '09:00 PM'),
                ('09:30 PM', '09:30 PM'),
                ('10:00 PM', '10:00 PM'),
                ('10:30 PM', '10:30 PM'),
                ('11:00 PM', '11:00 PM'),
                ('11:30 PM', '11:30 PM'), )

class Happyhour(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField('Address')
    time_start = models.CharField(
        max_length=10,
        choices=TIME_CHOICES,
        default=TIME_CHOICES[34][0],
    )
    time_end = models.CharField(
        max_length=10,
        choices=TIME_CHOICES,
        default=TIME_CHOICES[38][0],
    )
    added = models.DateField('Date review added/updated')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'Happyhour_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    happyhour = models.ForeignKey(Happyhour, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for happyhour_id: {self.happyhour_id} @{self.url}"