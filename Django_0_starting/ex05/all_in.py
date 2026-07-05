from sys import argv, exit

def check_arguments():
    if len(argv) != 2:
        exit(1)

def convert_string_to_list(argument):
    arguments = argument.strip().split(",")
    return arguments

def remove_empty_field_list(list):
    final_list = []
    for element in list:
        cleaned_element = element.strip().title()
        if cleaned_element:
            final_list.append(cleaned_element)
    return final_list

def check_if_capital_or_state(list, states, capital_cities):
    for element in list:
        if element in states:
            state_code = states[element]
            capital = capital_cities.get(state_code)
            print(f"{capital} is the capital of {element}")
        elif element in capital_cities.values():
            capital_key = [key for key, value in capital_cities.items() if value == capital]
            if len(capital_key) != 0:
                state_to_find = [key for key, value in states.items() if value == capital_key[0]]
            print(f"{element} is the capital of {state_to_find[0]}")
        else:
            print(f"{element} is neither a capital city nor a state")


def main():
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
    check_arguments()
    list = convert_string_to_list(argv[1])
    final_list = remove_empty_field_list(list)
    check_if_capital_or_state(final_list, states, capital_cities)


if __name__ == "__main__":
    main()