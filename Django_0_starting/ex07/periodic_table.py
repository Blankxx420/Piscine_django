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

def get_html_boilerplate():
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Periodic Table</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <table>
        <tr>\n"""
    return html_template

def render_periodic_table(elements):
    html_template = get_html_boilerplate()
    column = 0
    buffer = ""
    for name, info in elements.items():
        while int(info["position"]) > column:
            buffer += "\t\t<td></td>\n"
            column += 1
        buffer += "\t\t<td>\n"
        buffer += f"\t\t\t<h4>{name}</h4>\n"
        buffer += "\t\t\t<ul>\n"

        buffer += f"\t\t\t\t<li>No: {info["number"]}</li>\n"
        buffer += f"\t\t\t\t<li>{info["small"]}</li>\n"
        buffer += f"\t\t\t\t<li>{info["molar"]}</li>\n"
        buffer += f"\t\t\t\t<li>{info["electron"]}</li>\n"
        buffer += "\t\t\t</ul>\n"
        buffer += "\t\t</td>\n"
        column += 1
        if column == 18:
            buffer += "\t\t</tr>\n\t\t<tr>\n"
            column = 0
        html_template += buffer
        buffer = ""
    return html_template


def main():
    check_arguments()
    list_lines = parse_data_from_file(argv[1])
    dict_elements = create_nested_dict_from_list(list_lines)
    html = render_periodic_table(dict_elements)
    print(html)


if __name__ == "__main__":
    main()