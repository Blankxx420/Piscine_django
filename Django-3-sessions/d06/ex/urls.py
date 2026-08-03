from django.urls import path

from .views import (
    downvote_tips,
    homepage,
    log_out_user,
    login_user,
    register,
    upvote_tips,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("register", register, name="register"),
    path("login", login_user, name="login"),
    path("logout", log_out_user, name="logout"),
    path("tip/<int:tip_id>/upvote", upvote_tips, name="upvote_tip"),
    path("tip/<int:tip_id>/downvote", downvote_tips, name="downvote_tip")
]
