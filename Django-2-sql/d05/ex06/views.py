import psycopg2
import psycopg2.extras
from django.http import HttpResponse
from django.shortcuts import render


def init(request):
    try:
        ps = psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        sql_buffer = """CREATE TABLE IF NOT EXISTS ex06_movies (
        title VARCHAR(64) UNIQUE NOT NULL,
        episode_nb INT PRIMARY KEY,
        opening_crawl TEXT,
        director VARCHAR(32) NOT NULL,
        producer VARCHAR(128) NOT NULL,
        release_date DATE NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

        sql_trigger = """CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now();
        NEW.created = OLD.created;
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();
        """
        with ps.cursor() as curs:
            curs.execute(sql_buffer)
            curs.execute(sql_trigger)
            ps.commit()
            curs.close()
        
        ps.close()
        return HttpResponse("OK")
        
    except (psycopg2.DatabaseError) as error:
        return HttpResponse(error)


        
    
def populate(request):
    try:
        ps = psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        sql_list_insert = [
            {"episode_nb": 1, "title": "The Phantom Menace", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "1999-05-19"},
            {"episode_nb": 2, "title":"Attack of the Clones", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "2002-05-16"},
            {"episode_nb": 3, "title": "Revenge of the Sith", "director":"George Lucas", "producer": "Rick McCallum", "release_date": "2005-05-19"},
            {"episode_nb": 4, "title": "A New Hope", "director":"George Lucas", "producer": "GaryKurtz, Rick McCallum", "release_date": "1977-05-25"},
            {"episode_nb": 5, "title": "The Empire Strikes Back", "director":" Irvin Kershner", "producer": "Gary Kutz, Rick McCallum", "release_date": "1980-05-17"},
            {"episode_nb": 6, "title": "Return of the Jedi", "director":"Richard Marquand", "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum", "release_date": "1983-05-25"},
            {"episode_nb": 7, "title": "The Force Awakens", "director":" J. J. Abrams", "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "release_date": "2015-12-11"},
            ]
        cursor = ps.cursor()
        status = []
        for element in sql_list_insert:
            try:
                sql_request = """
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)"""
                values = (
                    element["episode_nb"],
                    element["title"],
                    element["director"],
                    element["producer"],
                    element["release_date"]
                )
                cursor.execute(sql_request, values)
                ps.commit()
                status.append(f"{element['title']} : OK")
            except Exception as error:
                ps.rollback()
                status.append(f"{element['title']} : {error}")
        cursor.close()
        ps.close()
    except (psycopg2.DatabaseError) as error:
        return HttpResponse(error)
    html_output = "<br>".join(status)
    return HttpResponse(html_output)

def display(request):
    try:
        with psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            
            cursor.execute("SELECT * FROM ex06_movies")

            data = cursor.fetchall()
            if not data:
                return HttpResponse("No data available")
            headers = ["episode_nb", "title", "opening_crawl", "director", "producer", "release_date", "created", "updated"]
            context = {"movies_list": data, "headers": headers}
            return render(request, 'ex06/sql_table.html', context)
    except psycopg2.DatabaseError as database_error:
        print(database_error)

def update(request):
    if request.method == "POST":
        try:
            form_movie_id = request.POST.get("movie_id")
            form_opening_crawl = request.POST.get("opening_crawl")
            with psycopg2.connect(
                        database="formationdjango",
                        user="djangouser",
                        password="secret",
                        host="localhost"
                    ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("UPDATE ex06_movies SET opening_crawl = %s WHERE episode_nb = %s",(form_opening_crawl, form_movie_id))
                ps.commit()

        except Exception:
            return HttpResponse("No data avaible")
    try:
        with psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        ) as ps, ps.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            
            cursor.execute("SELECT episode_nb, title, opening_crawl FROM ex06_movies ORDER BY episode_nb;")
            movies = cursor.fetchall()
            context = {"movies": movies}
            return render(request, "ex06/update_form.html", context)
     
    except Exception as e:
        print("Erreur chargement films :", e)
        return HttpResponse("Error loading movies")