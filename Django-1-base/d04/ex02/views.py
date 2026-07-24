from django.shortcuts import render
from .forms import BasicForm
from django.conf import settings
from datetime import datetime
import os


def form_text(request):
    history = []
    log_file_path = settings.EX02_LOG_FILE
    if request.method == 'POST':
        form = BasicForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['text']
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log_entry = f"{timestamp} - {user_text}"

            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            with open(log_file_path, 'a') as file:
                file.write(log_entry + '\n')

            form = BasicForm()
    else:
        form = BasicForm()

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            for raw_line in file:
                line = raw_line.strip()
                if line:
                   parts = line.split(' - ', 1)
                   if len(parts) == 2:
                        history.append({'timestamp': parts[0], 'text': parts[1]})
    context = {
        'form': form,
        'history': history,
    }
    return render(request, 'ex02/form.html', context)