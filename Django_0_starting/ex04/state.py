from sys import argv, exit

def check_arguments():
    if len(argv) != 2 :
        exit(1)

def find_state_by_capital(capital):
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
        }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    capital_key = [key for key, value in capital_cities.items() if value == capital]
    if len(capital_key) != 0:
        state_to_find = [key for key, value in states.items() if value == capital_key[0]] 
        print(state_to_find[0])
    else:
        print("Unkown capital")

if __name__ == "__main__":
    check_arguments()
    find_state_by_capital(argv[1])
