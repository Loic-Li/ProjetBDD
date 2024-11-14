from pymongo import MongoClient
import os

# Connexion à MongoDB
try:
    client = MongoClient('localhost', 27017)
    db = client['airline_database']
    print("Connexion à MongoDB réussie.")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")

# Fonction générique pour insérer les données
def insert_data(file_name, collection_name, fields, transform_func=None):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(file_path):
        print(f"Erreur : le fichier {file_name} n'existe pas.")
        return

    collection = db[collection_name]
    collection.delete_many({})  # On nettoie la collection pour éviter les doublons

    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for ligne in f:
            champs = ligne.strip().split('\t')
            if len(champs) != len(fields):
                print(f"Erreur de format dans {file_name} : {ligne.strip()}")
                continue

            try:
                record = {
                    fields[i]: (transform_func[i](champs[i]) if transform_func and transform_func[i] else champs[i])
                    for i in range(len(fields))
                }
                data.append(record)
            except ValueError as e:
                print(f"Erreur de conversion pour la ligne : {ligne.strip()} dans {file_name}. Détails : {e}")

    # Insertion des données dans MongoDB
    if data:
        try:
            collection.insert_many(data)
            print(f"Données de {collection_name} insérées avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'insertion de {collection_name} : {e}")

# Appels pour chaque fichier avec leurs champs et transformations spécifiques
insert_data('AVIONS.txt', 'avions', ['NumAv', 'NomAv', 'CapAv', 'VilleAv'], [int, None, int, None])
insert_data('CLIENTS.txt', 'clients', ['NumClient', 'Nom', 'NumRue', 'Rue', 'CodePostal', 'Ville'])
insert_data('DEFCLASSES.txt', 'defclasses', ['CodeClass', 'NomClass', 'Tarif'])
insert_data('PILOTES.txt', 'pilotes', ['NumPilote', 'NomPilote', 'AnneeNaissance', 'Ville'])
insert_data('VOLS.txt', 'vols', ['CodeVol', 'VilleDepart', 'VilleArrivee', 'DateDepart', 'HeureDepart', 'DateArrivee', 'HeureArrivee', 'NumPil', 'NumAv'], [None, None, None, None, None, None, None, int, int])
insert_data('RESERVATIONS.txt', 'reservations', ['NumClient', 'CodeVol', 'Classe', 'NbPlaces'], [None, None, None, int])

print("Données insérées avec succès dans MongoDB.")


# Requêtes pour afficher les données
print("\n--- Avions ---")
avions = db['avions'].find()
for avion in avions:
    print(avion)

print("\n--- Clients ---")
clients = db['clients'].find()
for client in clients:
    print(client)

print("\n--- Définitions de classes ---")
defclasses = db['defclasses'].find()
for defclass in defclasses:
    print(defclass)

print("\n--- Pilotes ---")
pilotes = db['pilotes'].find()
for pilote in pilotes:
    print(pilote)

print("\n--- Vols ---")
vols = db['vols'].find()
for vol in vols:
    print(vol)

print("\n--- Réservations ---")
reservations = db['reservations'].find()
for reservation in reservations:
    print(reservation)

print("Données affichées avec succès.")


# Jointure pour combiner les réservations avec les informations des clients et des vols
pipeline = [
    {
        '$lookup': {
            'from': 'clients',  # Nom de la collection à joindre
            'localField': 'NumClient',  # Champ dans la collection réservations
            'foreignField': 'NumClient',  # Champ dans la collection clients
            'as': 'client_info'  # Nom du champ pour stocker les informations des clients
        }
    },
    {
        '$lookup': {
            'from': 'vols',  # Nom de la collection à joindre
            'localField': 'CodeVol',  # Champ dans la collection réservations
            'foreignField': 'CodeVol',  # Champ dans la collection vols
            'as': 'vol_info'  # Nom du champ pour stocker les informations des vols
        }
    }
]

# Exécution de la jointure
reservations_jointes = db['reservations'].aggregate(pipeline)

# Affichage des résultats
for reservation in reservations_jointes:
    print(reservation)
