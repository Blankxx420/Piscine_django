
def print_number_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            print(line.strip().replace(',', '\n'))

if __name__ == "__main__":
    print_number_from_file("numbers.txt")
 