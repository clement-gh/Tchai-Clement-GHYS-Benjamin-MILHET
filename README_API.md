# TCHAI

## API de gestion de transactions

### Langages
Pour réaliser notre API, nous avons utiliser le langage Python avec le framework Flask permettant le dévelopement web avec Python. Pour le stockage des données, nous utilisons le système de gestion de base de données clé-valeur Redis qui est de type NoSQL.

## Format de la base de données REDIS

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

## Fonctionnalités

 - [Récupération de l'ensemble des transactions](#récupération-de-lensemble-des-transactions)

### Récupération de l'ensemble des transactions

Permet de récupérer l'ensemble des transaction stocker dans la base de données REDIS.

#### Données reçues

Méthode : GET

Retourne l'ensemble des transactions sous ce format : 

```
{
  "date":"12/12/2023, 15:20:06",
  "donneur":"Benjamin",
  "receveur":"Clement",
  "valeur":"100"
}
```

#### Exemple de requête

```
curl -X GET  http://127.0.0.1:5000/getTransactions
```
