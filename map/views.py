from django.http import HttpResponse
from django.shortcuts import render


def show_map(request):
    return render(request, 'map.html')

