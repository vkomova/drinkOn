from django.db import models
from datetime import date
# from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

TIME_CHOICES = (('00:00:00', '00:00 AM'),
                ('00:30:00', '00:30 AM'),
                ('01:00:00', '01:00 AM'),
                ('01:30:00', '01:30 AM'),
                ('02:00:00', '02:00 AM'),
                ('02:30:00', '02:30 AM'),
                ('03:00:00', '03:00 AM'),
                ('03:30:00', '03:30 AM'),
                ('04:00:00', '04:00 AM'),
                ('04:30:00', '04:30 AM'),
                ('05:00:00', '05:00 AM'),
                ('05:30:00', '05:30 AM'),
                ('06:00:00', '06:00 AM'),
                ('06:30:00', '06:30 AM'),
                ('07:00:00', '07:00 AM'),
                ('07:30:00', '07:30 AM'),
                ('08:00:00', '08:00 AM'),
                ('08:30:00', '08:30 AM'),
                ('09:00:00', '09:00 AM'),
                ('09:30:00', '09:30 AM'),
                ('10:00:00', '10:00 AM'),
                ('10:30:00', '10:30 AM'),
                ('11:00:00', '11:00 AM'),
                ('11:30:00', '11:30 AM'),
                ('12:00:00', '12:00 PM'),
                ('12:30:00', '12:30 PM'),
                ('13:00:00', '01:00 PM'),
                ('13:30:00', '01:30 PM'),
                ('14:00:00', '02:00 PM'),
                ('14:30:00', '02:30 PM'),
                ('15:00:00', '03:00 PM'),
                ('15:30:00', '03:30 PM'),
                ('16:00:00', '04:00 PM'),
                ('16:30:00', '04:30 PM'),
                ('17:00:00', '05:00 PM'),
                ('17:30:00', '05:30 PM'),
                ('18:00:00', '06:00 PM'),
                ('18:30:00', '06:30 PM'),
                ('19:00:00', '07:00 PM'),
                ('19:30:00', '07:30 PM'),
                ('20:00:00', '08:00 PM'),
                ('20:30:00', '08:30 PM'),
                ('21:00:00', '09:00 PM'),
                ('21:30:00', '09:30 PM'),
                ('22:00:00', '10:00 PM'),
                ('22:30:00', '10:30 PM'),
                ('23:00:00', '11:00 PM'),
                ('23:30:00', '11:30 PM'), )

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
    # added = models.DateTimeField(default=timezone.now)
    # added = models.DateField(input_formats=['YYYY-MM-DD'], default=date.today)
    # added = models.DateTimeField(default=date.today, input_formats=['%Y-%m-%d'])
    added = models.DateField('Date review was added/updated')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'Happyhour_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    happyhour = models.ForeignKey(Happyhour, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for happyhour_id: {self.happyhour_id} @{self.url}"