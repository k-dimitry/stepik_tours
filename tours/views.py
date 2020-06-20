from random import shuffle

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View

import data

TOURS = data.tours


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404</h1>Ой, что то сломалось... Наша команда уже чинит эту проблему!')


def custom_handler500(request):
    return HttpResponseServerError('<h1>Ошибка 500</h1>Не перживайте, вы все делали правильно. '
                                   'Но мы этого не предусмотрели, уже чиним!')


class MainView(View):
    def get(self, request):
        random_tours = list(range(1, 17))
        shuffle(random_tours)
        random_tours = random_tours[:6]
        lst_of_tours = [{**TOURS.get(num), **{"id": num}} for num in random_tours]
        context = {
            'title': data.title,
            'subtitle': data.subtitle,
            'description': data.description,
            'departures': data.departures,
            'random_tours': lst_of_tours
        }
        return render(request, 'index.html', context=context)


class DepartureView(View):
    def get(self, request, departure):
        tours = []
        tour_counter = 0
        max_nights = float("-inf")
        min_nights = float("inf")
        max_price = float("-inf")
        min_price = float("inf")
        for key, value in TOURS.items():
            if value.get("departure") == departure:
                tours.append({**value, **{"id": key}})
                tour_counter += 1
                nights = value.get("nights")
                if nights > max_nights:
                    max_nights = nights
                if nights < min_nights:
                    min_nights = nights
                price = value.get("price")
                if price > max_price:
                    max_price = price
                if price < min_price:
                    min_price = price
        context = {
            'tours': tours,
            'title': data.title,
            'subtitle': data.subtitle,
            'description': data.description,
            'departure_direction': data.departures.get(departure),
            'tour_counter': tour_counter,
            "max_nights": max_nights,
            "min_nights": min_nights,
            "max_price": max_price,
            "min_price": min_price

        }
        return render(request, 'departure.html', context=context)


class TourView(View):
    def get(self, request, id):
        context = {
            **TOURS.get(id),
            **{"departure": data.departures.get(data.tours.get(id).get("departure")),
               'stars_count': int(data.tours.get(id).get("stars")) * "★"},
        }
        return render(request, 'tour.html', context=context)
