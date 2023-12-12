# TCHAI

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />

[![checkSyntax](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/actions/workflows/main.yml/badge.svg)](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/actions/workflows/main.yml)
[![Docker Image CI](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/actions/workflows/docker.yml/badge.svg)](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/actions/workflows/docker.yml)

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

## Fonctionnalités:
Cette API développée en python a pour but de pouvoir gérer des transactions entre des personnes. 

 - Enregistrer une transaction.
 - Afficher une liste de toutes les transactions dans l’ordre chronologique.
 - Afficher une liste des transactions dans l’ordre chronologique liées à une personne.
 - Afficher le solde du compte de la personne.
 - Charger des données comprenant deux personnes et deux transactions.
 - Vérification des transactions grâce à un hashage SHA-256 et basé sur le hash de la transaction précédente.
 - Utilisation de la cryptographie asymétrique afin d’assurer l’authenticité de l’expéditeur.

## Langages
Pour réaliser notre API, nous avons utiliser le langage Python avec le framework Flask permettant le dévelopement web avec Python. Pour le stockage des données, nous utilisons le système de gestion de base de données clé-valeur Redis qui est de type NoSQL.

## Documentations

 - [Readme de l'API](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/blob/main/README_API.md)
 - [Documentation du Dockerfile](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/blob/main/README_Dockerfile.md)
 - [TCHAI V1](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/blob/main/README_TCHAI_V1.md)
 - [TCHAI V2](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/blob/main/README_TCHAI_V2.md)
