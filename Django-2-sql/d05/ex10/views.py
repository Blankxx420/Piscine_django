import os
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .forms import SearchCharMovieForm
from .models import People, Planets, Movies


def research_char_movie(request):
    characters = []
    form = SearchCharMovieForm(request.POST or None)
    
    if form.is_valid():
        min_date = form.cleaned_data['Movies_minimum_release_date']
        max_date = form.cleaned_data['Movies_maximum_release_date']
        min_diameter = form.cleaned_data['Planet_diameter_greater_than']
        gender_choice = form.cleaned_data['Character_gender']
        
        movies_query = Movies.objects.filter(
            release_date__range=[min_date, max_date],
            characters__gender=gender_choice,
            characters__homeworld__diameter__gt=min_diameter
        ).distinct()

        for movie in movies_query:
            chars = movie.characters.filter(
                gender=gender_choice,
                homeworld__diameter__gt=min_diameter
            )
            for char in chars:
                characters.append({
                    'movie': movie,
                    'character': char
                })
    context = {
        'form': form,
        'characters': characters,
    }
    return render(request, 'ex10/research.html', context)


def populate(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'ex10_initial_data.json')
        
        if not os.path.exists(file_path):
            return HttpResponse("File not found at root project.", status=404)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Insertion des Planètes
        for item in data:
            if item.get('model') == 'ex10.planets':
                pk = item.get('pk')
                fields = item.get('fields', {})
                Planets.objects.update_or_create(
                    id=pk,
                    defaults={
                        'name': fields.get('name'),
                        'climate': fields.get('climate') or '',
                        'diameter': fields.get('diameter'),
                        'orbital_period': fields.get('orbital_period'),
                        'population': fields.get('population'),
                        'rotation_period': fields.get('rotation_period'),
                        'surface_water': fields.get('surface_water'),
                        'terrain': fields.get('terrain') or '',
                    }
                )

        # 2. Insertion des Personnages
        for item in data:
            if item.get('model') == 'ex10.people':
                pk = item.get('pk')
                fields = item.get('fields', {})
                homeworld_id = fields.get('homeworld') # Récupère l'ID numérique (ex: 59 ou None)
                
                # Recherche par ID (pk) et non par nom
                homeworld_obj = Planets.objects.filter(pk=homeworld_id).first() if homeworld_id else None

                People.objects.update_or_create(
                    id=pk,
                    defaults={
                        'name': fields.get('name'),
                        'birth_year': fields.get('birth_year') or '',
                        'gender': fields.get('gender') or '',
                        'eye_color': fields.get('eye_color') or '',
                        'hair_color': fields.get('hair_color') or '',
                        'height': fields.get('height'),
                        'mass': fields.get('mass'),
                        'homeworld': homeworld_obj, # Sera correctement lié ou mis à NULL pour Yoda
                    }
                )

        # 3. Insertion des Films et liaison Many-to-Many
        for item in data:
            if item.get('model') == 'ex10.movies':
                pk = item.get('pk')
                fields = item.get('fields', {})
                character_ids = fields.get('characters', [])

                # Utilisation de pk=pk au lieu de id=pk
                movie_obj, created = Movies.objects.update_or_create(
                    pk=pk,
                    defaults={
                        'title': fields.get('title'),
                        'episode_nb': fields.get('episode_nb'),
                        'opening_crawl': fields.get('opening_crawl') or '',
                        'director': fields.get('director') or '',
                        'producer': fields.get('producer') or '',
                        'release_date': fields.get('release_date'),
                    }
                )
                
                if character_ids:
                    movie_obj.characters.set(character_ids)

        return HttpResponse("Base de données peuplée avec succès !")

    except Exception as e:
        return HttpResponse(f"Erreur : {e}", status=500)