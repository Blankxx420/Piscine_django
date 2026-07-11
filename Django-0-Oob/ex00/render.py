from sys import argv, exit, stderr


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
            return file.read()
    except FileNotFoundError:
        stderr.write("Error: File not found\n")
        exit(1)
        
def get_vars_in_dict():
    try:
        import settings
        return {k: v for k, v in vars(settings).items() if not k.startswith("__")}
    except ImportError:
        stderr.write("Error: settings.py not found\n")
        exit(1)
def subsitute_var_in_html(template_content, vars_dict):
    try:
        html_content = template_content.format(**vars_dict)
        return html_content
    except KeyError as e:
        stderr.write(f"Error: Variable {e} required by template is missing in settings.py\n")
        exit(1)

def generate_html_file(html_content):
    output_file = argv[1].replace(".template", ".html")
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
    except Exception:
        stderr.write("Error: Could not write output file\n")
        exit(1)


def main():
    check_arguments()
    template_content = read_template_file()
    vars_dict = get_vars_in_dict()
    html_content = subsitute_var_in_html(template_content, vars_dict)
    generate_html_file(html_content)

    
if __name__ == "__main__":
    main()