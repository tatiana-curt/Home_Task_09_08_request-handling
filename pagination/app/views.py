
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.urls import reverse
import csv
from urllib.parse import urlencode
from app.settings import BUS_STATION_CSV
from django.core.paginator import Paginator


def index(request):

    return HttpResponseRedirect(f'{reverse("bus_stations")}?page=1')


def bus_stations(request):
    page = request.GET.get('page')

    context_raw = {
        'bus_stations': [],
        'current_page': page,
        'prev_page_url': None,
        'next_page_url': None,
    }

    def generator_context(path):
        bus_stations_all = []

        with open(path, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                bus_stations_dict = {'Name': row['Name'],
                                     'Street': row['Street'],
                                     'District': row['District']}
                bus_stations_all.append(bus_stations_dict)

        paginator = Paginator(bus_stations_all, 10)
        page_object = paginator.get_page(page)
        page_content = page_object.object_list
        for item in page_content:
            context_raw['bus_stations'].append(item)

        if page_object.has_next() == True:
            params = {'page': int(page) + 1}
            context_raw['next_page_url'] = f'?{urlencode(params, True)}'

        if page_object.has_previous() == True:
            params = {'page': int(page) - 1}
            context_raw['prev_page_url'] = f'?{urlencode(params, True)}'

        return context_raw

    context = generator_context(BUS_STATION_CSV)

    return render_to_response('index.html', context)

#
