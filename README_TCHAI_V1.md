# TCHAI

## TCHAI V1

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
Le script HACKV1.py permet de modifier une transaction dans la base de données REDIS. Le fait de modifier la valeur de la transaction permet de ne pas détecter la fraude. En effet, la fonction de vérification ne peut pas vérifier un changement de valeur, il faut alors créer une fonction de vérification de hash.

### Release
 - [Lien vers la release](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/releases/tag/V1)
 - [Lien vers la branche](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/tree/tchaiV1)
