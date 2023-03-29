import os
import shutil
import xml.etree.ElementTree as ET

# Dossier de destination par défaut
destination_folder = 'C:/path/to/destination/folder'

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
    local_path = location.replace('file://localhost/', '').replace('%20', ' ')
    genre = track.get('Genre') or 'sans genres'

    # Copie des musiques dans le sous-dossier "collection"
    new_path = os.path.join(collection_folder, os.path.basename(local_path))
    shutil.copy2(local_path, new_path)

    # Mise à jour de la location dans le fichier XML
    new_location = f"file://localhost/{new_path.replace(' ', '%20')}"
    track.set('Location', new_location)

    # Copie des musiques dans le sous-dossier "rangé"
    genre_folder = os.path.join(ranged_folder, genre)
    os.makedirs(genre_folder, exist_ok=True)
    shutil.copy2(new_path, os.path.join(genre_folder, os.path.basename(new_path)))

# Sauvegarde du nouveau fichier XML à la racine du dossier de destination
tree.write(os.path.join(destination_folder, 'rekordbox_updated.xml'), encoding='UTF-8', xml_declaration=True)
