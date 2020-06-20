from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404</h1>Ой, что то сломалось... Наша команда уже чинит эту проблему!')


def custom_handler500(request):
    return HttpResponseServerError('<h1>Ошибка 500</h1>Не перживайте, вы все делали правильно. '
                                   'Но мы этого не предусмотрели, уже чиним!')


class MainView(View):
    def get(self, request):
        return render(request, 'index.html')


class DepartureView(View):
    def get(self, request, departure):
        return render(request, 'departure.html')


class TourView(View):
    def get(self, request, id):
        return render(request, 'tour.html')
