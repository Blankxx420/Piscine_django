from sys import argv, exit, stderr

def check_arguments():
    if len(argv) != 2:
        stderr.write("Usage : You must provide file that is called periodic_table.txt\n")
        exit(1)
    else:
        if argv[1] != "periodic_table.txt":
            stderr.write("Error: Wrong file name \n")
            exit(1)



def main():
    check_arguments()


if __name__ == "__main__":
    main()