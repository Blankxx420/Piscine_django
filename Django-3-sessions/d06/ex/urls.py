from django.urls import path

from .views import homepage, register, login
urlpatterns = [
    path("", homepage, name="homepage"),
    path("login", login, name="homepage"),
    path("register", register, name="homepage")
]
