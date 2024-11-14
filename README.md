# Gestion des données aériennes avec Redis et MongoDB

Ce projet implémente des scripts Python pour gérer des données aériennes en utilisant Redis, MongoDB, et des filtres de Bloom. Voici les détails sur chaque script et les instructions pour leur exécution.

---

## **Prérequis**

### Installation des fichiers requis

- [Fichier texte utilisé](https://drive.google.com/file/d/1wukMVw9QaViaCyQZZDVbe_3hdcvOv2Eq/view)

### **Redis**
- Commandes pour démarrer Redis sur le port spécifique:
  ```bash
    redis-cli -p 6380
  ```
- Pour lancer le script **code-redis.py**:
    - S'assurer d'être dans dans le répertoire du projet
```bash
    python3 code-redis.py
```

## **Mise en place de MongoDB avec Docker**

### **Installation de Docker**
Assurez-vous que Docker est installé sur votre machine.

- [Guide d'installation Docker](https://docs.docker.com/get-docker/)

### **Lancement de MongoDB via Docker**

Exécutez les commandes suivantes pour créer et démarrer un conteneur MongoDB :

```bash
# Télécharger l'image MongoDB
docker pull mongo:latest

# Créer le conteneur et démarre immédiatement
docker run --name mongodb -d -p 27017:27017 mongo:latest

# Si le conteneur déjà créer
docker start mongodb
```
### **Exécution du script code-mongo.py**
- Vérifiez que MongoDB fonctionne correctement en utilisant Docker :
```bash
    docker ps
```
- Une fois MongoDB actif, exécutez le script :
```bash
    python3 code-mongo.py
```

### **Filtres de Bloom**
- Redis BloomFilter est également installer avec docker
```bash
    # Création du conteneur de redis bloom
    docker run -d --name redis-bloom -p 6381:6381 redislabs/rebloom:latest

    # Lancement si déjà créer
    docker start redis-bloom
```

### Exécution du script **Bloom.py**

```bash
    python3 Bloom.py
```
