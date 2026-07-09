from sys import argv, exit, stderr
from os import rename


def check_arguments():
    file_extension = ".template"
    if len(argv) != 2:
        stderr.write("Error: Wrong number of argument expected 1\n")
        exit(1)
    elif not argv[1].endswith(file_extension):
        stderr.write("Error: Wrong file extension expected .template\n")
        exit(1)

def read_template_file():
    try:
        with open(argv[1], 'r', encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        stderr.write("Error: File not found\n")
        
def main():
    check_arguments()
    read_template_file()

if __name__ == "__main__":
    main()