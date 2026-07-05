from sys import argv, exit

def check_arguments():
    if len(argv) != 2:
        exit(1)

def find_capital(country_name): 
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
    if country_name in states:
        state_code = states[country_name]
        if state_code in capital_cities:
            print(capital_cities[state_code])
    else:
        print("Unknow state")
    

if __name__ == "__main__":
    check_arguments()
    find_capital(argv[1])