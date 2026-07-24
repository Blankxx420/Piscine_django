from django.shortcuts import render

def ex03_table(request):
    # En-têtes des colonnes
    headers = ["Noir", "Rouge", "Bleu", "Vert"]
    
    table_rows = []

    for i in range(50):
        factor = int(i * (255 / 50))
        
        c_noir = f"rgb({factor}, {factor}, {factor})"
        c_rouge = f"rgb({255 - factor}, 0, 0)"
        c_bleu = f"rgb(0, 0, {255 - factor})"
        c_vert = f"rgb(0, {255 - factor}, 0)"
        
        row = [c_noir, c_rouge, c_bleu, c_vert]
        table_rows.append(row)
        
    context = {
        'headers': headers,
        'table_rows': table_rows,
    }
    return render(request, 'ex03/table.html', context)