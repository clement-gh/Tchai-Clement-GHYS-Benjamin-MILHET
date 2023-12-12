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
 - [Récupération des transactions pour une personne](#récupération-des-transactions-pour-une-personne)
 - [Enregistrement d'une nouvelle transaction](#enregistrement-dune-nouvelle-transaction)
 - [Récupération du solde d'une personne](#récupération-du-solde-dune-personne)
 - [Vérification de l'ensemble des transactions](#vérification-de-lensemble-des-transactions)

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
status : 200
```

#### Exemple de requête

```
curl -X GET  http://127.0.0.1:5000/getTransactions
```

### Récupération des transactions pour une personne

Permet de récupérer l'ensemble des transaction stocker dans la base de données REDIS pour une personne.

#### Données envoyées

Méthode : POST

```
{
    "nom": "Nom de l'utilisateur",
}
```

#### Données reçues

Retourne l'ensemble des transactions sous ce format : 

```
{
    "date":"12/12/2023, 15:20:06",
    "donneur":"Benjamin",
    "receveur":"Clement",
    "valeur":"100"
}
status : 200
```

#### Exemple de requête

```
curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"nom\":\"Benjamin\"}" http://localhost:5000/getTransactionsParPersonne
```

### Enregistrement d'une nouvelle transaction

Permet d'enregistrer une nouvelle transaction.

#### Données envoyées

Méthode : POST

```
{
    "donneur": "Nom du donneur",
    "receveur": "Nom du receveur",
    "valeur": "Valeur de la transaction",
    "date": "Date et heure de la transaction",
    "hash": "Hash pour la sécurité de la transaction",
}
```

#### Données reçues

```
message : "La transaction a été enregistrée."
status : 200

ou

message : "La dernière transaction n'est pas valide."
status : 400
```

#### Exemple de requête

```
curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"donneur\":\"Benjamin\", \"receveur\":\"Clement\", \"valeur\":\"100\"}" http://localhost:5000/enregisterTransaction
```

### Récupération du solde d'une personne

Permet de récupérer le solde d'une personne.

#### Données envoyées

Méthode : POST

```
{
    "nom": "Nom de l'utilisateur",
}
```

#### Données reçues

Retourne le solde de la personne sous ce format :

```
message : 100
status : 200
```

#### Exemple de requête

```
curl -X GET  http://localhost:5000/getSolde?nom=Benjamin
```

### Vérification de l'ensemble des transactions

Permet de vérifier l'ensemble des transactions.

#### Données reçues

Méthode : GET

Retourne l'ensemble des transactions sous ce format : 

```
message : "Toutes les transactions sont valides."
status : 200

ou

message : "La transaction id n'est pas valide."
status : 400
```

#### Exemple de requête

```
curl -X GET  http://localhost:5000/verifierTransactions
```
