#!/bin/sh

#!/bin/sh

pip3 --version

LOG_FILE="install_path.log"

pip3 install --target=./local_lib -U git+https://github.com/jaraco/path.git > "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "Installation réussie ! Lancement de mon_programme..."
    python3 my_program.py
else
    echo "Erreur lors de l'installation de path.py. Vérifie le fichier $LOG_FILE"
    exit 1
fi