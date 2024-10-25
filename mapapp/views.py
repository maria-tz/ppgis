from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
from django.conf import settings
from .forms import PinForm
from .models import Pin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.db import migrations
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage

def update_image_paths(apps, schema_editor):
    Pin = apps.get_model('mapapp', 'Pin')  # Adjust 'yourapp' to your app name
    for pin in Pin.objects.all():
        if pin.image.name.startswith('C:/media/'):
            new_path = pin.image.name.replace('C:/media/', '')
            pin.image.name = new_path
            pin.save()

class Migration(migrations.Migration):
    dependencies = [
        ('mapapp', '0001_initial'),  # Adjust according to your migration dependencies
    ]

    operations = [
        migrations.RunPython(update_image_paths),
    ]

def delete_pin(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    
    # Delete the image file from the file system
    if pin.image and default_storage.exists(pin.image.name):
        default_storage.delete(pin.image.name)
    
    # Delete the pin from the database
    pin.delete()
    
    return JsonResponse({'success': True})


def load_geojson(file_name):
    try:
        # Build the path to the GeoJSON file
        file_path = os.path.join(settings.BASE_DIR, file_name)  # Adjust as needed
        print(f"Attempting to load GeoJSON file at: {file_path}")  # Debugging line
        with open(file_path, 'r') as geojson_file:
            data = json.load(geojson_file)
        print(f"Loaded data: {data}")  # Check content of loaded file
        return data
    except FileNotFoundError:
        print("File not found:", file_name)  # Log which file is missing
        return {'error': 'File not found'}

# Views to return geojson with safe=False
def geojson_historic_center(request):
    return JsonResponse(load_geojson('StrovolosHistoricCenter.geojson'), safe=False)

def geojson_boundaries(request):
    return JsonResponse(load_geojson('Strovolos_Boundaries.geojson'), safe=False)

def geojson_nicosia_green(request):
    return JsonResponse(load_geojson('Nicosia_Green.geojson'), safe=False)

def geojson_pedieos_landmarks(request):
    return JsonResponse(load_geojson('Pedieos_landmarks.geojson'), safe=False)

def pins_data(request):
    pins = Pin.objects.all().values('id', 'latitude', 'longitude', 'image')
    pin_list = []
    
    for pin in pins:
        pin['image'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, pin['image']))
        pin_list.append(pin)
        print(pin['image'])  # Debugging line to log the image URLs
    
    return JsonResponse(pin_list, safe=False)


#def pins_data(request):
    #pins = Pin.objects.all().values('latitude', 'longitude', 'image')
    # Modify the image URL to include MEDIA_URL


def map_view(request):
    form = PinForm()

    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            #image_url = fs.url(filename)  # This should return something like '/media/pins/filename'
            #print(f"Image URL being saved: {image_url}")  # Debugging line
            pin = Pin.objects.create(latitude=latitude, longitude=longitude, image=filename)
            pin.save()
            return redirect('map')

    return render(request, 'mapapp/map.html', {'form': form})