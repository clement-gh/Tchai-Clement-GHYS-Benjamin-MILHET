# TCHAI

## API de gestion de transactions

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
