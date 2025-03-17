import os
import csv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# 🔹 1️⃣ Définition des constantes
SCOPES = ["https://www.googleapis.com/auth/youtube"]
TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = "client_secret.json"

def get_credentials():
    """Gère l'authentification et retourne les credentials OAuth."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Rafraîchir le token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_profil():
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    request = youtube.channels().list(
        part = "snippet",
        mine = True
    )
    response = request.execute()
    channel_title = response['items'][0]['snippet']['title']
    return channel_title
    
def reset_compte():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print(f"Le token a été supprimé de {TOKEN_FILE}.")
    else:
        print(f"Aucun token trouvé à supprimer dans {TOKEN_FILE}.")
    get_profil()

def restaure_playlist(backup_file, playlist_name="Playlist_restaurée"):
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": playlist_name, "description": "Playlist restaurée depuis un backup"},
            "status": {"privacyStatus": "private"}
        },
        )
    response = request.execute()
    new_playlist_id = response["id"]
    print(f"✅ Nouvelle playlist créée : {playlist_name} (ID: {new_playlist_id})")

    # 2️⃣ Lire le fichier CSV et ajouter les vidéos à la playlist
    with open(backup_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            video_url = row["URL"]
            video_id = video_url.split("v=")[1]

            try:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": new_playlist_id,
                            "resourceId": {"kind": "youtube#video", "videoId": video_id}
                        }
                    },
                ).execute()
                print(f"✅ Vidéo ajoutée : {video_url}")
            except Exception as e:
                print(f"❌ Erreur sur {video_url} : {e}")

    print("\n🎉 Restauration terminée !")

def get_youtube_service():
    """Crée et retourne un client YouTube API."""
    creds = get_credentials()
    return build("youtube", "v3", credentials=creds)

def get_youtube_playlists(youtube):
    """Récupère les playlists de l'utilisateur."""
    playlists = []
    try:
        request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
        while request:
            response = request.execute()
            for item in response["items"]:
                playlists.append({"Nom": item["snippet"]["title"], "ID": item["id"]})
            request = youtube.playlists().list_next(request, response)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des playlists : {e}")
    return playlists

def get_videos_from_playlist(youtube, playlist_id):
    """Récupère les vidéos d'une playlist spécifique tout en ignorant les erreurs individuelles."""
    videos = []
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
    
    while request:
        try:
            response = request.execute()
            print(f"🔄 Récupération d'un lot de {len(response['items'])} vidéos...")
            
            for item in response["items"]:
                try:
                    title = item["snippet"]["title"]
                    video_id = item["snippet"]["resourceId"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    channel_title = item["snippet"]["videoOwnerChannelTitle"]
                    videos.append({"Titre": title, "Chaine": channel_title, "URL": video_url})
                except KeyError as e:
                    print(f"⚠️ Erreur avec une vidéo, clé manquante : {e} (vidéo ignorée)")

            request = youtube.playlistItems().list_next(request, response)

        except Exception as e:
            print(f"❌ Erreur lors de la récupération des vidéos de la playlist {playlist_id} : {e}")
            break  # Si c'est une erreur critique (ex: API down), on arrête totalement

    print(f"✅ Playlist complète récupérée ({len(videos)} vidéos)")
    return videos
