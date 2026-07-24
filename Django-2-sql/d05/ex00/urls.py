from django.urls import path
from .views import ex00

urlpatterns = [
    path('init', ex00, name="ex00")
]
