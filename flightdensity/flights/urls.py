from django.urls import path
from .views import *

urlpatterns = [
    path('', flightsGraph),
    path('all_in_one/', all_in_one),
    path('download/', download),
    path('parse/', parse)
]
