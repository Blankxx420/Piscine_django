from django.http import HttpResponse
import psycopg2

def ex00(request):
    try:
        ps = psycopg2.connect(
            database="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost"
        )
        sql_buffer = """CREATE TABLE IF NOT EXISTS ex00_movies (
        title VARCHAR(64) UNIQUE NOT NULL,
        episode_nb INT PRIMARY KEY,
        opening_crawl TEXT,
        director VARCHAR(32) NOT NULL,
        producer VARCHAR(128) NOT NULL,
        release_date DATE NOT NULL
        );"""
        
        with ps.cursor() as curs:
            curs.execute(sql_buffer)
            ps.commit()
            
        ps.close()
        return HttpResponse("OK")
        
    except (psycopg2.DatabaseError) as error:
        return HttpResponse(error)