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

def main():
    check_arguments()
    list_lines = parse_data_from_file(argv[1])


if __name__ == "__main__":
    main()