from django.db import models


# Create your models here.
class Flights(models.Model):
    number = models.CharField(max_length=255)
    sh_time = models.TimeField()
    sh_date = models.DateField()
    eta_time = models.TimeField()
    eta_date = models.DateField()
    airport_iata = models.CharField(max_length=3)
    is_depart = models.BooleanField()
    plane_type = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255)
