from django.shortcuts import render, redirect
from flights.models import Flights
import flights.parsing
from flights.parsing import *
from .forms import *
import json
from datetime import datetime
from pytz import timezone


def flightsGraph(request):
    day_for_seek = datetime.today().astimezone(tz=timezone("Asia/Novosibirsk")).date().strftime('%Y-%m-%d')
    if request.method == 'POST':
        form = DatePicker(request.POST)
        if form.is_valid():
            day_for_seek = form.cleaned_data["date_wig"]
    else:
        form = DatePicker({'date_wig': datetime.today()})

    all_flights = Flights.objects.filter(eta_date=day_for_seek)
    depart_fights = all_flights.filter(is_depart=1)
    arrive_flights = all_flights.filter(is_depart=0)

    count_by_hours_all = []
    count_by_hours_dep = []
    count_by_hours_arr = []
    for i in range(24):
        count_by_hours_all.append(all_flights.filter(eta_time__hour=i).count())
        count_by_hours_dep.append(depart_fights.filter(eta_time__hour=i).count())
        count_by_hours_arr.append(arrive_flights.filter(eta_time__hour=i).count())
    count_by_hours_all = json.dumps(count_by_hours_all)
    count_by_hours_dep = json.dumps(count_by_hours_dep)
    count_by_hours_arr = json.dumps(count_by_hours_arr)

    context = {
        'title': "Самолеты в толмачево",
        'data': {
            'data1': count_by_hours_all,
            'data2': count_by_hours_dep,
            'data3': count_by_hours_arr
        },
        'form': form
    }
    return render(request, 'flights/index.html', context)


def download(request):
    flights.parsing.save_tolmachovo_tables("/home/django_user/flights/flightdensity/flights/saved pages")
    return flightsGraph(request)


def parse(request):
    flights.parsing.parse_saved_tolmachovo_html("/home/django_user/flights/flightdensity/flights/saved pages/page.html")
    flights.parsing.parse_saved_tolmachovo_html("/home/django_user/flights/flightdensity/flights/saved pages/page_tomorrow.html")
    return flightsGraph(request)


def all_in_one(request):
    flights.parsing.save_tolmachovo_tables("/home/django_user/flights/flightdensity/flights/saved pages")
    flights.parsing.parse_saved_tolmachovo_html("/home/django_user/flights/flightdensity/flights/saved pages/page.html")
    flights.parsing.parse_saved_tolmachovo_html("/home/django_user/flights/flightdensity/flights/saved pages/page_tomorrow.html")
    return flightsGraph(request)
