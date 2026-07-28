from django.urls import path

from .views import research_char_movie, populate

urlpatterns = [
    path('', research_char_movie, name="research"),
    path('populate', populate, name="populate")
]