import csv
import time
import redis

# Connexion à Redis
r = redis.StrictRedis(host='localhost', port=6381, db=0)

# Nom du filtre de Bloom
filter_name = 'my_filter'

# Supprimer le filtre de Bloom s'il existe déjà
try:
    # Vérifier si le filtre de Bloom existe
    exists = r.execute_command('BF.EXISTS', filter_name, 'dummy_word')
    if exists:  # Si le filtre existe, le supprimer
        r.execute_command('BF.DEL', filter_name)
except redis.exceptions.ResponseError:
    # Ignore l'erreur si le filtre n'existe pas
    pass

# Création du filtre de Bloom
try:
    r.execute_command('BF.RESERVE', filter_name, 0.01, 100000)
except redis.exceptions.ResponseError as e:
    print(f"Erreur lors de la création du filtre de Bloom : {e}")

# Liste pour stocker les mots
word_list = []

# Lecture du fichier CSV
try:
    with open('DEM-1_1.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 2:  # Vérifier que la ligne n'est pas vide et qu'elle a au moins 2 colonnes
                word = row[0]  # Supposons que le mot est dans la première colonne
                definition = row[1]  # Supposons que la définition est dans la deuxième colonne
                # Ajout au filtre de Bloom
                r.execute_command('BF.ADD', filter_name, word)
                # Ajout à la liste
                word_list.append(word)
except FileNotFoundError:
    print("Erreur : Le fichier 'DEM-1_1.csv' n'a pas été trouvé. Assurez-vous que le fichier est dans le bon répertoire.")

# Mesurer le temps d'appartenance pour le filtre de Bloom
start_time_bloom = time.time()
for i in range(100000):
    r.execute_command('BF.EXISTS', filter_name, word_list[i % len(word_list)])
end_time_bloom = time.time()

# Mesurer le temps d'appartenance pour la liste
start_time_list = time.time()
for i in range(100000):
    word_list[i % len(word_list)] in word_list
end_time_list = time.time()

# Afficher les résultats
print(f'Temps d\'appartenance pour le Bloom filter : {end_time_bloom - start_time_bloom} secondes')
print(f'Temps d\'appartenance pour la liste : {end_time_list - start_time_list} secondes')
