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
    <h1>Mendeleev Periodic Table of Elements</h1>
    <h2>">Table Overview</h2>
    <h3>Chemical Elements</h3>
    <table>
        <tr>
"""
    return html_template

def render_periodic_table(elements):
    column = 0
    buffer = ""
    
    for name, info in elements.items():
        while column < int(info["position"]):
            buffer += "\t\t\t<td></td>\n"
            column += 1
            
        bg_class = "other-nonmetal"
        if column == 0 and name != "Hydrogen":
            bg_class = "alkali-metal"
        elif column == 1:
            bg_class = "alkaline-earth"
        elif 2 <= column <= 11:
            bg_class = "transition-metal"
        elif column == 16:
            bg_class = "halogen"
        elif column == 17:
            bg_class = "noble-gas"

        buffer += f'\t\t\t<td class="element-card {bg_class}">\n'
        buffer += f"\t\t\t\t<h4>{name}</h4>\n"
        buffer += "\t\t\t\t<ul>\n"
        buffer += f"\t\t\t\t\t<li>No: {info['number']}</li>\n"
        buffer += f"\t\t\t\t\t<li>Symbol: {info['small']}</li>\n"
        buffer += f"\t\t\t\t\t<li>Molar: {info['molar']}</li>\n"
        buffer += f"\t\t\t\t\t<li>Electron: {info['electron']}</li>\n"
        buffer += "\t\t\t\t</ul>\n"
        buffer += "\t\t\t</td>\n"
        
        column += 1

        if column == 18:
            column = 0
            if name != "Ununoctium": 
                buffer += "\t\t</tr>\n\t\t<tr>\n"    
    return buffer

def render_html_footer():
    html_footer = """\t\t</tr>
    </table>
</body>
</html>"""
    return html_footer

def create_html_file(elements):
    html_buffer = get_html_boilerplate()
    html_buffer += render_periodic_table(elements)
    html_buffer += render_html_footer()

    with open("periodic_table.html", 'w') as file:
        file.write(html_buffer)

def create_css_file():
    css_buffer = """table {
    border-collapse: collapse;
    margin: 30px auto;
    font-family: Arial, sans-serif;
}

td {
    width: 85px;
    height: 110px;
    padding: 4px;
    vertical-align: top;
    box-sizing: border-box; /* Évite que les bordures agrandissent la case */
}

/* Uniquement pour les cases avec un élément chimique */
.element-card {
    border: 1px solid #444;
    background-color: #f5f5f5;
    border-radius: 4px;
}

.element-card h4 {
    margin: 2px 0 6px 0;
    font-size: 12px;
    text-align: center;
    color: #222;
}

.element-card ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    font-size: 10px;
}

.element-card li {
    margin-bottom: 2px;
}
.noble-gas {
    background-color: #e8daef;
    border-color: #9b59b6;
}

.halogen {
    background-color: #d1f2eb;
    border-color: #16a085;
}

.alkali-metal {
    background-color: #fadbd8;
    border-color: #e74c3c;
}

.alkaline-earth {
    background-color: #fdebd0;
    border-color: #f39c12;
}

.transition-metal {
    background-color: #eaecee;
    border-color: #7f8c8d;
}

.other-nonmetal {
    background-color: #d5f5e3;
    border-color: #2ecc71;
}"""
    with open("style.css", 'w') as file:
        file.write(css_buffer)

def main():
    check_arguments()
    list_lines = parse_data_from_file(argv[1])
    dict_elements = create_nested_dict_from_list(list_lines)
    create_css_file()
    create_html_file(dict_elements)


if __name__ == "__main__":
    main()