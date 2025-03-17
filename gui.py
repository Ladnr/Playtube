import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from playtube import main as backup_playlists  # Import de la fonction principale
from youtube_api import restaure_playlist as restaure_playlist
from youtube_api import get_profil as get_profil
from youtube_api import reset_compte as reset_compte

BACKUP_FOLDER = "backup"
name_profil = ""
selected_backup_name = None  # Variable globale pour stocker le backup sélectionné

def list_backups():
    """Retourne la liste des dossiers de backup triés par date (du plus récent au plus ancien)."""
    user_folder = os.path.join(BACKUP_FOLDER, name_profil)  # 🔹 Chemin vers le dossier du compte
    if not os.path.exists(user_folder):
        print("trouve pas")
        return []
    
    backups = [f for f in os.listdir(user_folder) if os.path.isdir(os.path.join(user_folder, f))]
    return sorted(backups, reverse=True)

def list_files_in_backup(backup_name):
    """Retourne la liste des fichiers CSV d'un backup spécifique."""
    user_folder = os.path.join(BACKUP_FOLDER, name_profil)  # Ajout du dossier utilisateur
    backup_path = os.path.join(user_folder, backup_name)
    if not os.path.exists(backup_path):
        return []
    return [f for f in os.listdir(backup_path) if f.endswith(".csv")]

def on_backup_select(event):
    """Affiche les fichiers CSV du backup sélectionné."""
    global selected_backup_name
    selection = backup_listbox.curselection()
    
    if not selection:
        return  # Évite l'erreur si aucune sélection

    selected_backup_name = backup_listbox.get(selection[0]) 
    files = list_files_in_backup(selected_backup_name)
    
    file_listbox.delete(0, tk.END)  # Vider la liste actuelle
    for file in files:
        file_listbox.insert(tk.END, file)
    
    # Activer le bouton Restaurer si des fichiers sont présents
    if files:
        restore_button.config(state=tk.NORMAL)
    else:
        restore_button.config(state=tk.DISABLED)

def refresh_backup_list():
    """Rafraîchit la liste des backups après une nouvelle sauvegarde."""
    backup_listbox.delete(0, tk.END)
    for backup in list_backups():
        backup_listbox.insert(tk.END, backup)

def refresh_and_backup():
    # Fait la backup and refresh quand le bouton créer une backup est appuyé
    backup_playlists()
    refresh_backup_list()
    messagebox.showinfo("Succès", "Backup créée avec succès !")  # Confirme à l'utilisateur

def restore_selected_playlist():
    global selected_backup_name  # Utilise la variable globale

    if not selected_backup_name:  # Vérifie si un backup est sélectionné
        messagebox.showwarning("Erreur", "Sélectionnez un backup !")
        return


    # Vérifier si un fichier CSV est sélectionné
    file_selection = file_listbox.curselection()
    if not file_selection:
        messagebox.showwarning("Erreur", "Sélectionnez un fichier CSV !")
        return
    selected_file = file_listbox.get(file_selection[0])

    backup_path = os.path.join(BACKUP_FOLDER, name_profil, selected_backup_name, selected_file)

    # Demander un nom pour la nouvelle playlist
    playlist_name = tk.simpledialog.askstring("Nom de la playlist", "Entrez le nom de la playlist restaurée :")
    if not playlist_name:
        return

    restaure_playlist(backup_path, playlist_name)
    messagebox.showinfo("Succès", "Playlist restaurée avec succès !")

def change_account():
    reset_compte()  # Supprime le token et lance une nouvelle authentification
    update_profile_name()  # Met à jour le nom du profil affiché

def update_profile_name():
    """Met à jour le label avec le nouveau nom du profil utilisateur."""
    global name_profil  # Récupère le nom du profil
    name_profil = get_profil().replace(" ", "_")
    profil_label.config(text=f"Connecté en tant que : {name_profil}")  # Met à jour le texte du label
    refresh_backup_list()
    file_listbox.delete(0, tk.END)


name_profil = get_profil().replace(" ", "_")  # Récupère le nom du profil

root = tk.Tk()
root.title("Youtube Playlist Backup Manager")
root.geometry("500x500")

frame_profil = tk.Frame(root)
frame_profil.pack(pady=10)

# Label pour afficher le nom du profil
profil_label = tk.Label(frame_profil, text="", font=("Arial", 12, "bold"), justify=tk.LEFT)
profil_label.pack(side="left", padx=10)

# Bouton pour changer de compte
reset_button = tk.Button(frame_profil, text="Changer de compte", justify=tk.RIGHT, command=change_account)
reset_button.pack(side="right")

tk.Label(root, text="Sélectionnez un backup :", font=("Arial", 12, "bold")).pack(pady=5)
backup_listbox = tk.Listbox(root, height=8)
backup_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

tk.Label(root, text="Fichiers CSV :", font=("Arial", 12, "bold")).pack(pady=5)
file_listbox = tk.Listbox(root, height=8)
file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

update_profile_name()

# 🚀 Bouton Création backup (désactivé pour l’instant)
create_button = tk.Button(root, text="Créer une backup", command=refresh_and_backup)
create_button.pack(side='left', pady=10)

# 🚀 Bouton Restaurer (désactivé pour l’instant)
restore_button = tk.Button(root, text="Restaurer la Playlist", command=restore_selected_playlist)
restore_button.pack(side='right',pady=10)

# 🎯 Charger la liste des backups
refresh_backup_list()

# 🔄 Lier l’événement de sélection
backup_listbox.bind("<<ListboxSelect>>", on_backup_select)

root.mainloop()