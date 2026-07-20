from sys import argv, exit, stderr
import requests
from bs4 import BeautifulSoup

class LinkFinder:

    def __init__(self):
        self.depth = 0
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


def check_arguments():
    if len(argv) != 2:
        stderr.write("Error wrong number of arguments : Expected 1\n")
        exit(1)
    elif len(argv[1]) == 0:
        stderr.write("Error invalid arguments : Expected a none empty string\n")
        exit(1)


            

if __name__ == "__main__":
    check_arguments()