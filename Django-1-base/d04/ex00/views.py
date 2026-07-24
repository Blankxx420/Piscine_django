from django.shortcuts import render

def ex00(request):
    return render(request, "ex00/index.html")
