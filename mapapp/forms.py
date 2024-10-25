# mapapp/forms.py
from django import forms
from django.db import models
from .models import Pin  # Import the Pin model


class PinForm(forms.Form):
    latitude = forms.FloatField(label="Latitude", required=True)
    longitude = forms.FloatField(label="Longitude", required=True)
    image = forms.ImageField(label="Upload Image", required=True)