# mapapp/urls.py

from django.urls import path
from .views import map_view, pins_data, delete_pin, geojson_historic_center, geojson_boundaries, geojson_nicosia_green, geojson_pedieos_landmarks  # Ensure all views are imported
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', map_view, name='map'),  # Home page that shows the map
    path('pins_data/', pins_data, name='pins_data'),  # Pins data endpoint
    path('delete_pin/<int:pin_id>/', delete_pin, name='delete_pin'),  # Delete pin endpoint
    path('geojson_historic_center/', geojson_historic_center, name='geojson_historic_center'),  # Historic center GeoJSON
    path('geojson_boundaries/', geojson_boundaries, name='geojson_boundaries'),  # Boundaries GeoJSON
    path('geojson_nicosia_green/', geojson_nicosia_green, name='geojson_nicosia_green'),  # Nicosia Green GeoJSON
    path('geojson_pedieos_landmarks/', geojson_pedieos_landmarks, name='geojson_pedieos_landmarks'),  # Pedieos Landmarks GeoJSON
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
