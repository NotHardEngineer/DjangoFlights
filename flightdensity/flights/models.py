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

    def __str__(self):
        return self.number

class Companies(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    logo = models.ImageField(upload_to="photos/logo/")
    primary_color = models.CharField(max_length=6, default='000000')
    secondary_color = models.CharField(max_length=6, default='#bb33dd')

    def __str__(self):
        return self.name