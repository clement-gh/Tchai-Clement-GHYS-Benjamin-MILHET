# TCHAI

## TCHAI V2

### Langages
Pour réaliser notre API, nous avons utiliser le langage Python avec le framework Flask permettant le dévelopement web avec Python. Pour le stockage des données, nous utilisons le système de gestion de base de données clé-valeur Redis qui est de type NoSQL.

### Fonctionnalités
Cette API développée en python a pour but de pouvoir gérer des transactions entre des personnes. 

     - Enregistrer une transaction.
     - Afficher une liste de toutes les transactions dans l’ordre chronologique.
     - Afficher une liste des transactions dans l’ordre chronologique liées à une personne.
     - Afficher le solde du compte de la personne.
     - Charger des données comprenant deux personnes et deux transactions.
     - Vérification des transactions grâce à un hashage SHA-256.

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

### Release
 - [Lien vers la release](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/releases/tag/V2)
 - [Lien vers la branche](https://github.com/clement-gh/Tchai-Clement-GHYS-Benjamin-MILHET/tree/tchaiV2)