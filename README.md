# TCHAI

## TCHAI V1

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />

L'objectif du projet est de concevoir un système de transactions électroniques avec une intégrité continue.

## Membres du groupe
 - Clément GHYS - clement_ghys@etu.u-bourgogne.fr
 - Benjamin MILHET - benjamin_milhet@etu.u-bourgogne.fr

## Lancement des conteneurs

### DOCKER BUILD 
```
docker-compose build
```

### DOCKER RUN
```
docker-compose up
```

### Langages
Pour réaliser notre API, nous avons utiliser le langage Python avec le framework Flask permettant le dévelopement web avec Python. Pour le stockage des données, nous utilisons le système de gestion de base de données clé-valeur Redis qui est de type NoSQL.

### Fonctionnalités
Cette API développée en python a pour but de pouvoir gérer des transactions entre des personnes. 

     - Enregistrer une transaction.
     - Afficher une liste de toutes les transactions dans l’ordre chronologique.
     - Afficher une liste des transactions dans l’ordre chronologique liées à une personne.
     - Afficher le solde du compte de la personne.
     - Charger des données comprenant deux personnes et deux transactions.

### Format de la base de données REDIS

```
Redis
├── rUser - 0
│   ├── nom.user : nom de l'utilisateur (String)
│   ├── transaction.user : Liste des id des transactions (Array)
│   └── solde.user : Solde de la personne (Float)
│
├── rTransaction - 1
│   ├── transaction.id.donneur : Nom du donneur dans une transaction (String)
│   ├── transaction.id.receveur : Nom du receveur dans une transaction (String)
│   ├── transaction.id.valeur : Valeur de la transaction (Float)
│   └── transaction.id.date : Date et heure a laquelle transaction se déroule (DateTime)
```

### Script HACKV1
Le script HACKV1.py permet de modifier une transaction dans la base de données REDIS. Le fait de modifier la valeur de la transaction permet de ne pas détecter la fraude. En effet, la fonction de vérification ne peut pas vérifier un changement de valeur, il faut alors hasher chaque transaction et ajouter une fonction pour vérifier l'intégriter des transactions.

### Release
 - [Lien vers la release](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/releases/tag/V1)
 - [Lien vers la branche](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/tree/tchaiV1)
