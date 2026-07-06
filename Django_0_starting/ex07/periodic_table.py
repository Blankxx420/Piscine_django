from sys import argv, exit, stderr

def check_arguments():
    if len(argv) != 2:
        stderr.write("Usage : You must provide file that is called periodic_table.txt\n")
        exit(1)
    else:
        if argv[1] != "periodic_table.txt":
            stderr.write("Error: Wrong file name \n")
            exit(1)

def parse_data_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip().replace(",", "").splitlines()
    
def create_nested_dict_from_list(list):
    elements = {}
    for line in list:
        element_name, data = line.split('=')
        element_name = element_name.strip()
        data_cleaned = data.replace(': ', ':')
        internal_dict = {}
        for block in data_cleaned.split():
            if ':' in block:
                key, value = block.split(':')
                internal_dict[key] = value
        elements[element_name] = internal_dict
    return elements

def main():
    check_arguments()
    list_lines = parse_data_from_file(argv[1])
    dict_elements = create_nested_dict_from_list(list_lines)


if __name__ == "__main__":
    main()