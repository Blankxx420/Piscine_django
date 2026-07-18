from sys import argv, exit, stderr
import requests

def check_arguments():
    if len(argv) != 2:
        stderr.write("Error wrong number of arguments : Expected 1\n")
        exit(1)
    elif len(argv[1]) == 0:
        stderr.write("Error invalid arguments : Expected a none empty string\n")
        exit(1)

def construct_url():
    search_word = argv[1].replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{search_word}"
    return url

def get_wikipedia_page():
    url = construct_url()
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        stderr.write(f"Network or Server Error: {e}\n")
        exit(1)

if __name__ == "__main__":
    check_arguments()
    repsonse = get_wikipedia_page()