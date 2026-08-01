from django.urls import path

from .views import homepage, register, login_user, log_out_user, upvote_tips, downvote_tips

urlpatterns = [
    path("", homepage, name="homepage"),
    path("register", register, name="register"),
    path("login", login_user, name="login"),
    path("logout", log_out_user, name="logout"),
    path("tip/<int:tip_id>/upvote", upvote_tips, name="upvote_tip"),
    path("tip/<int:tip_id>/downvote", downvote_tips, name="downvote_tip")
]
