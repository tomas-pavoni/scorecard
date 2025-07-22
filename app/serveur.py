# app/serveur.py
from pathlib import Path

# Crée un fichier pour vérifier si ce script est exécuté
log_path = Path(__file__).parent / "test_lancement.txt"

with open(log_path, "w") as f:
    f.write("✅ Le script serveur.py a bien été lancé depuis Tauri\n")
