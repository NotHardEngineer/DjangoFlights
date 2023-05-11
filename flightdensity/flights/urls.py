from django.urls import path
from .views import *

urlpatterns = [
    path('', all_in_one),
    path('graph_only/', flightsGraph),
    path('download/', download),
    path('parse/', parse)
]
