from django.urls import path
from .views import ex03_table

urlpatterns = [
    path("", ex03_table, name="ex03")
]
