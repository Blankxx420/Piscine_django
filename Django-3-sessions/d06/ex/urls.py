from django.urls import path

from .views import homepage, register, login_user, log_out_user

urlpatterns = [
    path("", homepage, name="homepage"),
    path("register", register, name="register"),
    path("login", login_user, name="login"),
    path("logout", log_out_user, name="logout")
]
