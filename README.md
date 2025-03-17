
# Playtube - YouTube Playlist Backup Manager

Playtube est une application Python permettant de sauvegarder et restaurer des playlists YouTube au format CSV. Elle offre une interface utilisateur via Tkinter et permet de gérer plusieurs comptes YouTube avec des sauvegardes séparées pour chaque utilisateur.

## Fonctionnalités
- Sauvegarde des playlists YouTube sous forme de fichiers CSV.
- Restauration des playlists à partir des sauvegardes.
- Gestion de plusieurs comptes YouTube (permet de se connecter et de changer de compte).
- Interface graphique conviviale avec Tkinter.

## Installation

### Prérequis
- Python 3.6 ou version ultérieure
- Accès à internet pour se connecter à l'API YouTube

### Étapes d'installation
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/playtube.git
   cd playtube
   ```

2. Créez un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   venv\Scripts\activate     # Sur Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration de l'API Google (client_secret.json)

Pour pouvoir utiliser ce projet, vous devez créer vos propres identifiants API dans la [Google Cloud Console](https://console.cloud.google.com/).

### Étapes :
1. Rendez-vous sur [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un projet ou utilisez un projet existant.
3. Allez dans **APIs & Services** > **Library** et activez l'API YouTube Data.
4. Allez dans **APIs & Services** > **Credentials** et créez un **OAuth 2.0 Client ID**.
5. Téléchargez le fichier `client_secret.json` et placez-le dans le dossier de votre projet local.

Le fichier `client_secret.json` contient vos informations d'authentification API. Il ne doit pas être partagé publiquement.

### Dépendances
- `google-api-python-client` : pour interagir avec l'API YouTube.
- `tkinter` : pour l'interface graphique.
- `pandas` : pour manipuler les données CSV.
- `requests` : pour gérer les requêtes HTTP.

## Utilisation

1. **Lancer l'application** : 
   Pour lancer l'application, exécutez le fichier `gui.py`:
   ```bash
   python gui.py
   ```

2. **Sauvegarde des playlists** : 
   Une fois connecté à votre compte YouTube, cliquez sur "Créer une backup" pour sauvegarder vos playlists sous forme de fichiers CSV dans le répertoire `backup/`.

3. **Restaurer une playlist** : 
   Pour restaurer une playlist, sélectionnez un backup et un fichier CSV, puis cliquez sur "Restaurer la Playlist".

4. **Changer de compte** : 
   Si vous voulez changer de compte, cliquez sur "Changer de compte", cela vous redirigera pour une nouvelle authentification.

## Structure du projet
```
playtube/
│
├── backup/               # Dossier des backups
├── gui.py                # Interface graphique
├── playtube.py           # Logique de gestion des playlists
├── youtube_api.py        # Interaction avec l'API YouTube
├── backup_manager.py     # Gestion des fichiers de sauvegarde
├── requirements.txt      # Liste des dépendances
└── README.md             # Documentation du projet
```

## Auteurs
- **Auteur**: [Ladnr](https://github.com/Ladnr)

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.