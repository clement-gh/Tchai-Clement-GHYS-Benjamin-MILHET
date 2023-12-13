# TCHAI

## TCHAI V4
L'amélioration principale de cette version est l'ajout de la cryptographie asymétrique. Cela permet d'assurer l'authenticité du donneur dans la transaction et aini corriger les éventuelles atatques possibles de la version 3. 

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
     - Vérification des transactions grâce à un hashage SHA-256 et basé sur le hash de la transaction précédente.
     - Utilisation de la cryptographie asymétrique afin d’assurer l’authenticité de l’expéditeur.


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
│   ├── transaction.id.date : Date et heure a laquelle transaction se déroule (DateTime)
│   └── transaction.id.hash : Hash de sécurité pour la transaction (String)
```

### Cryptographie asymétrique
Pour assurer l'authenticité de l'expéditeur, nous avons utilisé la cryptographie asymétrique. En effet, nous avons généré une clé privée et une clé publique pour chaque utilisateur. L'utilisateur envoie sa clé publique au serveur pour qu'il puisse la stocker dans la base de données REDIS. Lorsqu'un utilisateur veut envoyer une transaction, il doit signer la transaction avec sa clé privée. Lorsque le serveur reçoit la transaction, il vérifie la signature avec la clé publique de l'utilisateur. Si la signature est valide, la transaction est enregistrée dans la base de données.

### Release
 - [Lien vers la release](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/releases/tag/V4)
 - [Lien vers la branche](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/tree/tchaiV4)
