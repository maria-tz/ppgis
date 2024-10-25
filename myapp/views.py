from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.http import JsonResponse
import json

def geojson_data(request):
    file_path = r'C:\Users\user\Documents\mywebapp\StrovolosHistoricCenter.geojson'  # Path to the uploaded file
    with open(file_path, 'r') as geojson_file:
        data = json.load(geojson_file)
    return JsonResponse(data)

def map_view(request):
    return render(request, 'mapapp/map.html')