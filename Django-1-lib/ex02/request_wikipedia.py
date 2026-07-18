from sys import argv, stderr, exit
import requests
import json
from dewiki.parser import Parser


def check_arguments():
    if len(argv) != 2:
        stderr.write("Error: Wrong number of arguments. Expected 1\n")
        exit(1)

def get_wiki_data_from_arg():
    try:      
        response = requests.get(
            url=f"https://en.wikipedia.org/w/api.php?action=parse&page={argv[1]}&format=json",
            headers={"User-Agent": "request_wikipedia.py (your_email@example.com)"},
            params={
                "action": "query",
                "titles": argv[1],
                "prop": "revisions",
                "rvprop": "content",
                "redirects": 1,
                "format": "json",
                "formatversion": 2
            }
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            stderr.write(f"Wikipedia Error: {data['error']['info']}\n")
            exit(1)
        return response.json()
    
    except requests.exceptions.RequestException as e:
        stderr.write(f"Network or HTTP Error: {e}\n")
        exit(1)
        
def clean_data_from_response(data):
    try:
        pages = data.get("query",{}).get("pages", [])
        if not pages or pages[0].get("missing"):
                stderr.write(f"Error: No Wikipedia page found for '{argv[1]}'.\n")
                exit(1)
        wiki_text = pages[0]["revisions"][0]["content"]
        cleaned_text = Parser().parse_string(wiki_text)
        return cleaned_text
    
    except requests.exceptions.RequestException as e:
        stderr.write(f"Network or Server Error: {e}\n")
        exit(1)
    except (KeyError, IndexError, json.JSONDecodeError):
        stderr.write("Error: Failed to parse Wikipedia API response.\n")
        exit(1)

def write_cleaned_text_to_file(clean_text):
    with open(f"{argv[1]}.wiki", 'w') as file:
        file.write(clean_text)

if __name__ == "__main__":
    check_arguments()
    data = get_wiki_data_from_arg()
    clean_text = clean_data_from_response(data)
    write_cleaned_text_to_file(clean_text)