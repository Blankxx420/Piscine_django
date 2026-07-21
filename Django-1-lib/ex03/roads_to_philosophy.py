from sys import argv, exit, stderr
import requests
from bs4 import BeautifulSoup

class LinkFinder:

    def __init__(self):
        self.parenthesis_depth = 0
        self.namespaces = [
            "Help:", "File:", "Wikipedia:", "Category:", "Talk:", "Special:",
            "Portal:", "Template:", "Draft:", "User:", "MediaWiki:", "Module:",
            "WT:", "WP:"
        ]

    def is_href_valid(self, href):

        if not href or not href.startwith("/wiki/"):
            return False
        
        title_part= href[6:]
        for ns in self.namespaces:
            if title_part.startwith(ns):
                return False
        return True
    
    def is_italic(self, node):
        current = node
        while current and current.name != 'p':
            if current.name in ["i", "em"]:
                return True
            current = current.parent
        return False


def check_arguments():
    if len(argv) != 2:
        stderr.write("Error wrong number of arguments : Expected 1\n")
        exit(1)
    elif len(argv[1]) == 0:
        stderr.write("Error invalid arguments : Expected a none empty string\n")
        exit(1)

def make_request(url):
    header = {"User-Agent": "road_to_philosopy.py (your_email@example.com)"}
    try:
        response = requests.get(url, headers=header, timeout=10)
        if response.status_code == 404:
            print("It leads to a dead end !")
            exit(0)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        exit(1)


def main():
    check_arguments()

    search_term = argv[1]
    path = search_term.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{path}"

    while True:
        response = make_request(url)


            

if __name__ == "__main__":
    check_arguments()