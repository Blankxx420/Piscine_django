#!/bin/bash

# Créer le virtualenv s'il n'existe pas déjà
if [ ! -d "django_venv" ]; then
    python3 -m venv django_venv
fi

# Activer le virtualenv
source django_venv/bin/activate

# Mettre à jour pip et installer les requirements
pip install --upgrade pip
pip install -r requirement.txt