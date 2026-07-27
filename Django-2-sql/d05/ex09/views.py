from django.shortcuts import render

from .models import People


def display(request):
    characters = People.objects.filter(
        homeworld__climate__icontains='windy'
    ).order_by('name')

    context = {
        "characters": characters,
        "command_line": 'python3 manage.py loaddata ex09_initial_data.json'
    }
    return render(request, 'ex09/sql_table.html', context)