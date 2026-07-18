from sys import argv, stderr, exit
import requests
import json
from dewiki.parser import Parser


def check_arguments():
    if len(argv) != 2:
        stderr.write("Error: Wrong number of arguments. Expected 1\n")
        exit(1)


def get_wiki_data_from_arg():
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "titles": argv[1],
        "prop": "revisions",
        "rvprop": "content",
        "redirects": 1,
        "format": "json",
        "formatversion": 2
    }
    
    headers = {
        "User-Agent": "request_wikipedia.py (your_email@example.com)"
    }

    try:      
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            stderr.write(f"Wikipedia Error: {data['error']['info']}\n")
            exit(1)
        return data
    
    except requests.exceptions.RequestException as e:
        stderr.write(f"Network or HTTP Error: {e}\n")
        exit(1)


def clean_data_from_response(data):
    try:
        pages = data.get("query", {}).get("pages", [])
        if not pages or pages[0].get("missing"):
            stderr.write(f"Error: No Wikipedia page found for '{argv[1]}'.\n")
            exit(1)

        wiki_text = pages[0]["revisions"][0]["content"]
        cleaned_text = Parser().parse_string(wiki_text)
        return cleaned_text
    
    except (KeyError, IndexError):
        stderr.write("Error: Failed to parse Wikipedia API response structure.\n")
        exit(1)


def write_cleaned_text_to_file(clean_text):
    filename = f"{argv[1].replace(' ', '_')}.wiki"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(clean_text)
    except IOError as e:
        stderr.write(f"Error: Could not write to file {filename}. {e}\n")
        exit(1)


if __name__ == "__main__":
    check_arguments()
    data = get_wiki_data_from_arg()
    clean_text = clean_data_from_response(data)
    write_cleaned_text_to_file(clean_text)