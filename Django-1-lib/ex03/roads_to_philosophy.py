import sys
import urllib.parse
import requests
from bs4 import BeautifulSoup, NavigableString

class LinkFinder:
    def __init__(self):
        self.paren_depth = 0
        
        self.namespaces = [
            "Help:", "File:", "Wikipedia:", "Category:", "Talk:", "Special:",
            "Portal:", "Template:", "Draft:", "User:", "MediaWiki:", "Module:",
            "WT:", "WP:"
        ]

    def is_valid_href(self, href):
        """Vérifie et normalise le lien Wikipédia sans utiliser urllib."""
        if not href:
            return False
            
        if href.startswith("http://") or href.startswith("https://"):
            if "wikipedia.org/wiki/" not in href:
                return False
            idx = href.find("/wiki/")
            path = href[idx:]
        elif href.startswith("//"):
            if "wikipedia.org/wiki/" not in href:
                return False
            idx = href.find("/wiki/")
            path = href[idx:]
        elif href.startswith("/wiki/"):
            path = href
        else:
            return False

        title_part = path[6:]
        
        for ns in self.namespaces:
            if title_part.startswith(ns):
                return False
                
        return True

    def is_italic(self, node):
        """Vérifie si le nœud courant ou un de ses parents est en italique."""
        curr = node
        while curr and getattr(curr, 'name', None) != 'p':
            if getattr(curr, 'name', None) in ['i', 'em']:
                return True
            curr = curr.parent
        return False

    def search_node(self, node):
        """Parcourt récursivement les nœuds pour trouver le premier lien valide."""
        
        if type(node) is NavigableString:
            self.paren_depth += node.count('(') - node.count(')')
            return None

        if getattr(node, 'name', None) in ['sup', 'table', 'div']:
            return None

        if getattr(node, 'name', None) == 'a':
            if self.paren_depth <= 0 and self.is_valid_href(node.get('href')) and not self.is_italic(node):
                href = node.get('href')
                if '#' in href:
                    href = href.split('#')[0]
                return href
            
        if hasattr(node, 'children'):
            for child in node.children:
                res = self.search_node(child)
                if res:
                    return res
        return None

def get_first_valid_link(soup):
    """Trouve le premier lien valide dans les paragraphes d'introduction principaux."""
    content = soup.find(id="mw-content-text")
    if not content:
        return None
    
    parser_output = content.find(class_="mw-parser-output")
    if not parser_output:
        return None
    
    for p in parser_output.find_all('p'):
        
        if not p.text.strip():
            continue
            
        finder = LinkFinder()
        href = finder.search_node(p)
        
        if href:
            return href
            
    return None
            
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]
    path = search_term.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{path}"
    headers = {
        "User-Agent": "road_to_philosophy.py (your_email@example.com)"
    }
    roads = []

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 404:
                print("It leads to a dead end !")
                sys.exit(0)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'html.parser')

        redirect_msg = soup.find('span', class_='mw-redirectedfrom')
        if redirect_msg:
            a_tag = redirect_msg.find('a')
            if a_tag:
                orig_title = a_tag.text
                if orig_title in roads:
                    print("It leads to an infinite loop !")
                    sys.exit(0)
                roads.append(orig_title)
                print(orig_title)
                
        h1 = soup.find('h1', id='firstHeading')
        if not h1:
            print("Error: Could not find page title.")
            sys.exit(1)

        title = h1.text

        if title in roads:
            print("It leads to an infinite loop !")
            sys.exit(0)

        roads.append(title)
        print(title)
        
        if title == 'Philosophy':
            print(f"{len(roads)} roads from {roads[0]} to philosophy !")
            sys.exit(0)

        next_link = get_first_valid_link(soup)

        if not next_link:
            print("It leads to a dead end !")
            sys.exit(0)
            
        if not next_link:
            print("It leads to a dead end !")
            sys.exit(0)
            
        if next_link.startswith("http://") or next_link.startswith("https://"):
            url = next_link
        elif next_link.startswith("//"):
            url = "https:" + next_link
        else:
            url = "https://en.wikipedia.org" + next_link

if __name__ == '__main__':
    main()