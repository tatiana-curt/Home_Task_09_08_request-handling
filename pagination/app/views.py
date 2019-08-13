
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.urls import reverse
import csv
from urllib.parse import urlencode
from app.settings import BUS_STATION_CSV


def index(request):

    return redirect(urlencode(bus_stations))


def bus_stations(request):
    page = request.GET.get('page')

    context_raw = {
        'bus_stations': [],
        'current_page': page,
        'prev_page_url': None,
        'next_page_url': f'?page={int(page) + 1}',
    }

    def generator_context(path, cursor, count_input=10):
        with open(path, newline='') as csvfile:
            count = 0
            reader = csv.DictReader(csvfile)
            for i, line in enumerate(reader):
                if i == cursor:
                    for row in reader:
                        bus_stations_dict = {'Name': row['Name'],
                                             'Street': row['Street'],
                                             'District': row['District']}
                        context_raw['bus_stations'].append(bus_stations_dict)
                        count += 1
                        if count == count_input:
                            return context_raw

    cursor = int(page)*10-10
    context = generator_context(BUS_STATION_CSV, cursor, 10)
    return render_to_response('index.html', context)

# Вопросы:

# 1. по какой-то причине не читается первая строка в файле, хотя cursor для
# первой странеицы передается согласно формуле - page*10-10 и это будет "0", а значит первая строка.

# 2. Не могу придумать как красиво реализовать отображение послденийх строк в файле (которых не 10 а меньше)
# не хочеться прописывать отдельную обработку страницы номер 1081.
# по хорошему нужно наверно проверять пустая ли строка (row) в функции generator_context
# и если  row == None возвращать в context_raw то что успело заполниться, но такая проверка через условие почему-то не проходит.