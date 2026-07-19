from sys import argv, exit, stderr
import requests
from bs4 import BeautifulSoup

def check_arguments():
    if len(argv) != 2:
        stderr.write("Error wrong number of arguments : Expected 1\n")
        exit(1)
    elif len(argv[1]) == 0:
        stderr.write("Error invalid arguments : Expected a none empty string\n")
        exit(1)

def construct_url(word):
    search_word = word.replace(" ", "_")
    final_url = f"https://en.wikipedia.org/wiki/{search_word}"
    return final_url

def get_wikipedia_page(search_word):
    url = construct_url(search_word)
    header = {
        "User-Agent": "road_to_philosophy.py (your_email@example.com)"
    }
    try:
        response = requests.get(url=url, headers=header)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        stderr.write(f"Network or Server Error: {e}\n")
        exit(1)

def parse_response(response):
    bs = BeautifulSoup(response, "html.parser")
    id_bodycontent = bs.find(id="bodyContent")
    paragraphes = id_bodycontent.find_all("p")
    for p in paragraphes:
        p_tag = p.find("a")
        if p_tag is not None and p_tag.has_attr("title"):
            return p.find("a")["title"]
        0
def iter_to_philosophy():
    response = get_wikipedia_page(argv[1])
    link = parse_response(response)
    while link != "Philosophy":
        print(link)
        response = get_wikipedia_page(link)
        link = parse_response(response)
            

if __name__ == "__main__":
    check_arguments()
    iter_to_philosophy()