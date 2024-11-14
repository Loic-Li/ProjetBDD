# Gestion des données aériennes avec Redis et MongoDB

Ce projet implémente des scripts Python pour gérer des données aériennes en utilisant Redis, MongoDB, et des filtres de Bloom. Voici les détails sur chaque script et les instructions pour leur exécution.

---

## **Prérequis**

Avant de commencer, assurez-vous que les éléments suivants sont installés et configurés :

### **1. Redis**
- Version : ≥ 6.x
- Modules nécessaires : RedisBloom pour le filtre de Bloom.
- Commandes pour démarrer les instances Redis :
  ```bash
  redis-server --port 6380
  redis-server --port 6381
