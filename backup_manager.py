import os
import csv
from datetime import datetime
import pandas as pd

BACKUP_FOLDER = "backup"

def create_backup_folder(user_name):
    """Crée un dossier de sauvegarde basé sur la date actuelle."""
    user_backup_folder = os.path.join(BACKUP_FOLDER, user_name)
    os.makedirs(user_backup_folder, exist_ok=True)

    # Ajouter la date au nom du dossier pour éviter les collisions
    backup_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(user_backup_folder, backup_date)
    os.makedirs(backup_path, exist_ok=True)

    return backup_path

def export_to_csv(filepath, videos):
    """Exporte les vidéos d'une playlist en CSV."""
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Titre", "Chaine", "URL"])
            writer.writeheader()
            writer.writerows(videos)
        print(f"✅ Exporté : {filepath}")
    except Exception as e:
        print(f"❌ Erreur d'export CSV pour {filepath} : {e}")

def export_playlists_metadata(backup_path, playlists):
    """Sauvegarde la liste des playlists dans un CSV."""
    df = pd.DataFrame(playlists)
    metadata_path = os.path.join(backup_path, "playlists.csv")
    df.to_csv(metadata_path, index=False, encoding="utf-8")
    print(f"✅ Métadonnées exportées : {metadata_path}")