import os
import shutil
import urllib.parse
import xml.etree.ElementTree as ET

# Dossier de destination par défaut
destination_folder = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'Music_sorted')

# Lecture et analyse du fichier XML
tree = ET.parse('rekordbox.xml')
root = tree.getroot()

# Création des sous-dossiers "collection" et "rangé"
collection_folder = os.path.join(destination_folder, 'collection')
ranged_folder = os.path.join(destination_folder, 'rangé')

os.makedirs(collection_folder, exist_ok=True)
os.makedirs(ranged_folder, exist_ok=True)

# Parcours des pistes dans le fichier XML
for track in root.findall('.//TRACK'):
    location = track.get('Location')
    if location is None:
        print("Avertissement: Aucune location trouvée pour cette piste. Piste ignorée.")
        continue

    local_path = urllib.parse.unquote(
        location.replace('file://localhost/', ''))
    invalid_chars = '\\/:*?"<>|'
    genre = ''.join(c if c not in invalid_chars else '_' for c in track.get(
        'Genre', 'sans genres'))

    # Copie des musiques dans le sous-dossier "collection"
    new_path = os.path.join(collection_folder, os.path.basename(local_path))

    if not os.path.exists(new_path):
        try:
            shutil.copy2(local_path, new_path)
            print(f"Copié dans le dossier 'collection': '{new_path}'")
        except Exception as e:
            print(f"Erreur lors de la copie de '{local_path}': {e}")
    else:
        print(
            f"Le fichier existe déjà dans le dossier 'collection': '{new_path}'")

    # Mise à jour de la location dans le fichier XML
    new_location = f"file://localhost/{urllib.parse.quote(new_path)}"
    track.set('Location', new_location)

    # Copie des musiques dans le sous-dossier "rangé"
    genre_folder = os.path.join(ranged_folder, genre)
    os.makedirs(genre_folder, exist_ok=True)
    ranged_new_path = os.path.join(genre_folder, os.path.basename(new_path))

    if not os.path.exists(ranged_new_path):
        try:
            shutil.copy2(new_path, ranged_new_path)
            print(f"Copié dans le dossier 'rangé': '{ranged_new_path}'")
        except Exception as e:
            print(f"Erreur lors de la copie de '{new_path}': {e}")
    else:
        print(
            f"Le fichier existe déjà dans le dossier 'rangé': '{ranged_new_path}'")

# Sauvegarde du nouveau fichier XML à la racine du dossier de destination
tree.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rekordbox_updated.xml'),
           encoding='UTF-8', xml_declaration=True)
