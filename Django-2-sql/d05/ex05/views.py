from django.http import HttpResponse
from django.shortcuts import render

from .forms import DeleteMovieForm
from .models import Movies


def populate(request):
    list_to_insert = [
                {"episode_nb": 1, "title": "The Phantom Menace", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "1999-05-19"},
                {"episode_nb": 2, "title":"Attack of the Clones", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "2002-05-16"},
                {"episode_nb": 3, "title": "Revenge of the Sith", "director":"George Lucas", "producer": "Rick McCallum", "release_date": "2005-05-19"},
                {"episode_nb": 4, "title": "A New Hope", "director":"George Lucas", "producer": "GaryKurtz, Rick McCallum", "release_date": "1977-05-25"},
                {"episode_nb": 5, "title": "The Empire Strikes Back", "director":" Irvin Kershner", "producer": "Gary Kutz, Rick McCallum", "release_date": "1980-05-17"},
                {"episode_nb": 6, "title": "Return of the Jedi", "director":"Richard Marquand", "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum", "release_date": "1983-05-25"},
                {"episode_nb": 7, "title": "The Force Awakens", "director":" J. J. Abrams", "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "release_date": "2015-12-11"},
                ]
    status = []
    for row in list_to_insert:
        try:
            Movies.objects.create(
                episode_nb= row.get("episode_nb"),
                title = row.get("title"),
                director = row.get("director"),
                producer = row.get("producer"),
                release_date = row.get("release_date")
            )
            status.append(f"{row.get("title")}: ok")
        except Exception as error:
            status.append(f"{row.get("title")}: {error}")
    html_output = "<br>".join(status)
    return HttpResponse(html_output)
    
def display(request):
    try:
        all_movies = Movies.objects.all()
        headers = ["episode_nb", "title", "opening_crawl", "director", "producer", "release_date"]
        context = {"movies_list": all_movies, "headers": headers}
        return render(request, "ex03/sql_table.html", context)
    except (Exception):
        return HttpResponse("No data avaible")

def remove(request):
    if request.method == "POST":
        form = DeleteMovieForm(request.POST)
        if form.is_valid():
            movie_to_delete = form.cleaned_data['movie']
            movie_to_delete.delete()
            form = DeleteMovieForm()
    else:
        form = DeleteMovieForm()

    movies_left = Movies.objects.all()
    if not movies_left:
        return HttpResponse("No data available")

    context = {"form": form,}
    return render(request, "ex05/remove_form.html", context)