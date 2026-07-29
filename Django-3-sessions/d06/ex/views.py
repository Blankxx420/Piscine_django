import random

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone


def homepage(request: HttpRequest):
    try:
        if "username_expiration" not in request.session:
            username = random.choice(settings.ANONYMOUS_USERNAME)
            request.session['guest_username'] = username
            request.session['username_expiration'] =  timezone.now() + timezone.timedelta(seconds=42)
        else:
            if timezone.now() >= request.session.get('username_expiration'):
                username = random.choice(settings.ANONYMOUS_USERNAME)
                while username == request.session.get('guest_username'):    
                    username = random.choice(settings.ANONYMOUS_USERNAME)
                request.session['guest_username'] = username
                request.session['username_expiration'] =  timezone.now() + timezone.timedelta(seconds=42)
            else:
                username = request.session.get('guest_username')
        request.session.modified = True
        context = {"username": username}
        return render(request, "ex/nav.html", context)
    except Exception as error:
        return HttpResponse(error)