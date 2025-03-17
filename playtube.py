import os
from youtube_api import get_youtube_service, get_youtube_playlists, get_videos_from_playlist, get_profil
from backup_manager import create_backup_folder, export_to_csv, export_playlists_metadata

def main():

    youtube = get_youtube_service()

    # 📛 Récupération du nom du profil (ou ID)
    user_name = get_profil().replace(" ", "_")  # Remplace les espaces par des underscores pour éviter les problèmes de chemin
    
    # 📁 Création du dossier de backup spécifique à l'utilisateur
    backup_path = create_backup_folder(user_name)

    # 📋 Récupération des playlists
    playlists = get_youtube_playlists(youtube)
    if not playlists:
        print("⚠ Aucune playlist trouvée !")
        return

    # 🔄 Sauvegarde de chaque playlist en CSV
    for playlist in playlists:
        playlist_name = playlist["Nom"].replace("/", "-")  # Sécurité pour les noms de fichiers
        playlist_id = playlist["ID"]
        
        videos = get_videos_from_playlist(youtube, playlist_id)
        csv_path = os.path.join(backup_path, f"{playlist_name}.csv")
        export_to_csv(csv_path, videos)

    # 📜 Sauvegarde des métadonnées des playlists
    export_playlists_metadata(backup_path, playlists)
    
    print("\n🎉 Sauvegarde terminée avec succès ! 🎶")

if __name__ == "__main__":
    main()