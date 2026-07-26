from django.urls import path
from .views import populate, display, remove

urlpatterns = [
    path('populate', populate, name="populate"),
    path('display', display, name="display"),
    path('remove', remove, name="remove")
]