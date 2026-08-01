import random

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TipsForm
from .models import ModelTips


def homepage(request: HttpRequest):

    all_tips = ModelTips.objects.all().order_by('-date_creation')
    tipsform = TipsForm()

    if request.method == "POST" and request.user.is_authenticated:
        tipsform = TipsForm(request.POST)
        if tipsform.is_valid():
            tip = tipsform.save(commit=False)
            tip.author = request.user.username
            tip.save()
            return redirect("homepage")
        
    username = None
    if not request.user.is_authenticated:
        now = timezone.now()
        expiration = request.session.get('username_expiration')
        choices = getattr(settings, 'ANONYMOUS_USERNAME', ['Guest'])
        if "guest_username" not in request.session or not expiration or now >= expiration:
            username = random.choice(choices)
            if len(choices) > 1:
                while username == request.session.get('guest_username'):
                    username = random.choice(choices)
            request.session['guest_username'] = username
            request.session['username_expiration'] = now + timezone.timedelta(seconds=42)
            request.session.modified = True
        else:
            username = request.session.get('guest_username')

    context = {
        "username": username,
        "tips": all_tips,
        "tipsform": tipsform
    }
    return render(request, "ex/base.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("homepage")
        
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")    
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "ex/register.html", context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect("homepage")
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "ex/login.html", context)

@login_required
def log_out_user(request):
    logout(request)
    return redirect("homepage")

@login_required
def upvote_tips(request, tip_id):
    tip = get_object_or_404(ModelTips, id=tip_id)
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)
    
    if request.user in tip.upvotes.all():
        tip.upvotes.remove(request.user)
    else:
        tip.upvotes.add(request.user)
    return redirect("homepage")
