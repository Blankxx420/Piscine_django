import os

import psycopg2
import psycopg2.extras
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def init(request):

    sql_planet = """CREATE TABLE IF NOT EXISTS ex08_planets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    climate VARCHAR,
    diameter INT,
    orbital_period INT,
    population BIGINT,
    rotation_period INT,
    surface_water REAL,
    terrain VARCHAR(128)
    );"""

    sql_people = """CREATE TABLE IF NOT EXISTS ex08_people (
        id SERIAL PRIMARY KEY,
        name VARCHAR(64) UNIQUE NOT NULL,
        birth_year VARCHAR(32),
        gender VARCHAR(32),
        eye_color VARCHAR(32),
        hair_color VARCHAR(32),
        height INT,
        mass REAL,
        homeworld VARCHAR(64),
        CONSTRAINT fk_homeworld_planet FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
    );"""
    try:
        with psycopg2.connect(
                    database="formationdjango",
                    user="djangouser",
                    password="secret",
                    host="localhost"
                ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql_planet)
            cursor.execute(sql_people)
            ps.commit()
            return HttpResponse("OK")
    except (psycopg2.DatabaseError) as error:
            return HttpResponse(error)
    
def populate(request):
    status = []
    app_dir = os.path.dirname(__file__)
    
    imports = [
        {
            "table": "ex08_planets",
            "file": os.path.join(app_dir, "planets.csv"),
            "columns": "(name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)"
        },
        {
            "table": "ex08_people",
            "file": os.path.join(app_dir, "people.csv"),
            "columns": "(name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)"
        }
    ]

    try:
        with psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            
            for item in imports:
                try:
                    with open(item["file"], "r", encoding="utf-8") as file:
                        sql_copy = f"COPY {item['table']} {item['columns']} FROM STDIN WITH (FORMAT csv, DELIMITER '\t', NULL 'NULL')"
                        cursor.copy_expert(sql_copy, file)
                        status.append(f"{item['file'].split('/')[-1]}: OK")
                except Exception as error:
                    ps.rollback()
                    status.append(f"{item['file'].split('/')[-1]}: {error}")
            ps.commit()
    except Exception as error:
        return HttpResponse(error)
        
    html_output = "<br>".join(status)
    return HttpResponse(html_output)

def display(request):
    try:
        sql_query = """
        SELECT people.name AS PEOPLE_NAME,
           planet.name AS PLANET_NAME,
           planet.climate AS PLANET_CLIMATE
        FROM ex08_people people
        JOIN ex08_planets planet ON people.homeworld = planet.name
        WHERE planet.climate ILIKE '%windy%'
        ORDER BY people.name ASC;
    """
        with psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql_query)
            result_query = cursor.fetchall()
            context = {"data_query": result_query}
            return render(request, "ex08/sql_table.html", context)
    except Exception:
        return HttpResponse("No data avaible")

         