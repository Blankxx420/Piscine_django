from django.urls import path

from .views import init, populate, display

urlpatterns = [
    path('init', init, name="init"),
    path('populate', populate, name="populate"),
    path('display', display, name="display"),
]