import redis
import json
from pathlib import Path

# Connexion à Redis
r = redis.StrictRedis(host='localhost', port=6380, db=0, charset="utf-8", decode_responses=True)

# Chemin relatif basé sur le dossier du script
base_dir = Path(__file__).parent

# Fonction pour lire les avions
def read_avions(file_path):
    avions = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 4:
                    print(f"Erreur de format dans AVIONS: {ligne.strip()}")
                    continue

                try:
                    num_av = int(champs[0])  # Convertir en entier
                    nom_av = champs[1].strip()  # Nom de l'avion
                    cap_av = int(champs[2])  # Capacité en entier
                    ville_av = champs[3].strip()  # Ville

                    avions[num_av] = {
                        'NumAv': num_av,
                        'NomAv': nom_av,
                        'CapAv': cap_av,
                        'VilleAv': ville_av
                    }
                except ValueError as e:
                    print(f"Erreur de conversion pour la ligne : {ligne.strip()}. Détails : {e}")
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return avions


# Fonction pour lire les clients
def read_clients(file_path):
    clients = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 6:
                    continue
                num_client, nom, num_rue, rue, code_postal, ville = champs
                clients[num_client] = {
                    'NumClient': num_client,
                    'Nom': nom,
                    'NumRue': num_rue,
                    'Rue': rue,
                    'CodePostal': code_postal,
                    'Ville': ville
                }
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return clients

# Fonction pour lire les différentes classes
def read_defclasses(file_path):
    defclasses = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 3:
                    continue
                code_class, nom_class, tarif = champs
                defclasses[(code_class, nom_class)] = {
                    'Classe': nom_class,
                    'CoeffPrix': tarif
                }
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return defclasses

# Fonction pour lire les pilotes
def read_pilotes(file_path):
    pilotes = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 4:
                    continue
                num_pilote, nom_pilote, annee_naissance, ville = champs
                pilotes[num_pilote] = {
                    'NumPilote': num_pilote,
                    'NomPilote': nom_pilote,
                    'AnneeNaissance': annee_naissance,
                    'Ville': ville
                }
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return pilotes

# Fonction pour lire les vols
def read_vols(file_path):
    vols = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 9:
                    print(f"Erreur de format dans VOLS: {ligne.strip()}")
                    continue
                champs = [champ.strip() for champ in champs]
                code_vol, ville_depart, ville_arrivee, date_depart, heure_depart, date_arrivee, heure_arrivee, num_pil, num_av = champs

                vols[code_vol] = {
                    'CodeVol': code_vol,
                    'VilleDepart': ville_depart,
                    'VilleArrivee': ville_arrivee,
                    'DateDepart': date_depart,
                    'HeureDepart': heure_depart,
                    'DateArrivee': date_arrivee,
                    'HeureArrivee': heure_arrivee,
                    'NumPil': int(num_pil),
                    'NumAv': int(num_av)
                }
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return vols

# Fonction pour lire les réservations
def read_reservations(file_path):
    reservations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                champs = ligne.strip().split('\t')
                if len(champs) != 4:
                    continue
                num_client, code_vol, classe, nb_places = champs
                reservations.append({
                    'NumClient': num_client,
                    'CodeVol': code_vol,
                    'Classe': classe,
                    'NbPlaces': int(nb_places)
                })
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    return reservations

# Fonction principale pour créer et insérer des réservations dans Redis
def create_reservations(avions_file, clients_file, defclasses_file, pilotes_file, vols_file, reservations_file):
    avions = read_avions(avions_file)
    clients = read_clients(clients_file)
    defclasses = read_defclasses(defclasses_file)
    pilotes = read_pilotes(pilotes_file)
    vols = read_vols(vols_file)
    reservations = read_reservations(reservations_file)

    # Insérer chaque entité dans Redis
    for num_av, avion in avions.items():
        r.set(f'avion:{num_av}', json.dumps(avion))

    for num_pil, pilote in pilotes.items():
        r.set(f'pilote:{num_pil}', json.dumps(pilote))

    for num_client, client in clients.items():
        r.set(f'client:{num_client}', json.dumps(client))

    for code_vol, vol in vols.items():
        r.set(f'vol:{code_vol}', json.dumps(vol))

    for key, classe in defclasses.items():
        r.set(f'defclass:{key[0]}:{key[1]}', json.dumps(classe))

    # Créer les réservations dans Redis
    reservation_list = []
    for res in reservations:
        vol_data = vols.get(res['CodeVol'], {})
        client_data = clients.get(res['NumClient'], {})
        avion_data = avions.get(vol_data.get('NumAv'), {})

        reservation = {
            'vol': vol_data,
            'avion': avion_data,
            'client': client_data,
            'NbPlaces': res['NbPlaces']
        }
        r.set(f'reservation:{res["NumClient"]}:{res["CodeVol"]}:{res["Classe"]}', json.dumps(reservation))
        reservation_list.append(reservation)

    return reservation_list

# Utilisation pour créer et afficher les réservations
reservations = create_reservations(
    base_dir / 'AVIONS.txt',
    base_dir / 'CLIENTS.txt',
    base_dir / 'DEFCLASSES.txt',
    base_dir / 'PILOTES.txt',
    base_dir / 'VOLS.txt',
    base_dir / 'RESERVATIONS.txt'
)

print(json.dumps(reservations, indent=4))


def count_pilotes_in_reservations():
    # Récupérer toutes les clés des réservations stockées dans Redis
    reservations_keys = r.keys('reservation:*')  # Cela récupère toutes les clés comme 'reservation:client_id:code_vol:classe'

    pilotes_count = set()  # Utilisation d'un set pour éviter les doublons

    # Parcours de chaque clé de réservation
    for key in reservations_keys:
        reservation_data = r.get(key)

        if reservation_data:
            reservation = json.loads(reservation_data)
            vol_data = reservation.get('vol', {})

            if 'NumPil' in vol_data:
                pilotes_count.add(vol_data['NumPil'])

    return len(pilotes_count)  # Retourne le nombre unique de pilotes dans les réservations


def get_unique_villes_arrivee():
    # Récupérer toutes les clés des vols stockés dans Redis
    vols_keys = r.keys('vol:*')

    villes_arrivee = set()

    # Parcours de chaque clé de vol
    for key in vols_keys:
        vol_data = r.get(key)

        if vol_data:
            vol = json.loads(vol_data)
            villes_arrivee.add(vol['VilleArrivee'])

    return list(villes_arrivee)



# Exemple d'utilisation


# Utilisation pour récupérer toutes les villes d'arrivée uniques dans une variable
villes_arrivee_uniques = get_unique_villes_arrivee()

# Affichage des villes d'arrivée sans doublons
print("Villes d'arrivée :", villes_arrivee_uniques)



# Afficher le résultat
nombre_pilotes = count_pilotes_in_reservations()
print(f"Nombre de pilotes dans les réservations : {nombre_pilotes}")







def search_pilotes_in_reservations_by_letter(letter):
    # Récupérer toutes les clés des réservations stockées dans Redis
    reservations_keys = r.keys('reservation:*')  # Cela récupère toutes les clés comme 'reservation:client_id:code_vol:classe'

    pilotes_found = set()  # Utilisation d'un set pour éviter les doublons

    # Parcours de chaque clé de réservation
    for key in reservations_keys:
        reservation_data = r.get(key)

        if reservation_data:
            reservation = json.loads(reservation_data)
            vol_data = reservation.get('vol', {})

            # Vérifie si le NumPil est présent dans les données du vol
            if 'NumPil' in vol_data:
                num_pilote = vol_data['NumPil']  # Récupère le numéro du pilote

                # Récupérer les données du pilote depuis Redis
                pilote_data = r.get(f'pilote:{num_pilote}')

                if pilote_data:
                    pilote = json.loads(pilote_data)  # Convertit les données JSON en dictionnaire Python
                    nom_pilote = pilote.get('NomPilote', '')  # Récupère le nom du pilote

                    # Vérifie si la lettre est présente dans le nom du pilote (insensible à la casse)
                    if letter.lower() in nom_pilote.lower():
                        pilotes_found.add(num_pilote)  # Ajoute le numéro du pilote à l'ensemble pour éviter les doublons

    return len(pilotes_found)  # Retourne le nombre de pilotes trouvés



# Exemple de recherche de pilotes avec une lettre donnée
lettre_recherche = 'a'  # Lettre à rechercher
pilotes_trouves = search_pilotes_in_reservations_by_letter(lettre_recherche)

# Afficher les résultats
print(f"Pilotes trouvés dont le nom contient la lettre '{lettre_recherche}':")
print(json.dumps(pilotes_trouves, indent=4))

def join_reservations():
    # Récupérer toutes les clés des réservations stockées dans Redis
    reservations_keys = r.keys('reservation:*')
    jointures = []

    for key in reservations_keys:
        reservation_data = r.get(key)

        if reservation_data:
            reservation = json.loads(reservation_data)

            # Join with the client data
            client_data = r.get(f'client:{reservation["client"]["NumClient"]}')
            if client_data:
                reservation['client'] = json.loads(client_data)  # Add client details to reservation

            # Join with the vol data
            vol_data = reservation.get('vol', {})
            if 'NumPil' in vol_data:
                pilote_data = r.get(f'pilote:{vol_data["NumPil"]}')
                if pilote_data:
                    reservation['pilot'] = json.loads(pilote_data)  # Add pilot details to reservation

            jointures.append(reservation)

    return jointures

# Call the join function
reservations_jointes = join_reservations()
print(json.dumps(reservations_jointes, indent=4))
