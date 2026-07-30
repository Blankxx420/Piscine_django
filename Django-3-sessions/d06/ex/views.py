import random

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone


def homepage(request: HttpRequest):
    try:
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
            
        context = {"username": username}
        return render(request, "ex/base.html", context)
        
    except Exception as error:
        return HttpResponse(f"Erreur interne : {error}", status=500)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")    
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "ex/register.html", context)
    