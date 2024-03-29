import calendar
import time

from flask import Flask, request
import sys
import redis
import json
import hashlib
import datetime

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization

from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})

rUser = redis.Redis(host='TCHAI_redis', port=6379, db=0, decode_responses=True)
rTransaction = redis.Redis(host='TCHAI_redis', port=6379, db=1, decode_responses=True)


@app.route("/")
def hello_world():
    return "Hello, world!", 200


@app.route("/getAllUsers", methods=['GET'])
def get_all_users():
    """
        Permet de récupérer tous les utilisateurs au format JSON

        :return: Un JSON contenant tous les utilisateurs
    """
    # curl -X GET  http://127.0.0.1:5000/getAllUsers

    liste_res = []
    tmp = rUser.keys("nom.*")
    for i in range(len(tmp)):
        liste_res.append(tmp[i][4:])
    return liste_res, 200


@app.route("/getTransactions", methods=['GET'])
def get_transactions():
    """
        Renvoie la liste des transactions

        :return: liste des transactions
    """
    # curl -X GET  http://127.0.0.1:5000/getTransactions

    liste_res = []
    liste_transaction = get_list_transaction()

    for j, transaction in enumerate(liste_transaction):
        valid = verifier_une_transaction(transaction) if j == 0 else verifier_une_transaction(transaction,
                                                                                              liste_transaction[j - 1])

        if not valid:
            return f"La transaction {transaction} n'est pas valide.", 400

        transaction_key = f"transaction.{transaction}."
        liste_res.append({
            "donneur": rTransaction.get(transaction_key + "donneur"),
            "receveur": rTransaction.get(transaction_key + "receveur"),
            "valeur": rTransaction.get(transaction_key + "valeur"),
            "date": rTransaction.get(transaction_key + "date")
        })

    return liste_res, 200


@app.route("/getTransactionsParPersonne", methods=['POST'])
def get_transactions_par_personne():
    """
        Renvoie la liste des transactions pour une personne

        :param: nom de la personne

        :return: liste des transactions de la personne
    """
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"nom\":\"Benjamin\"}" http://localhost:5000/getTransactionsParPersonne

    data = request.get_json()
    nom = data.get('nom')

    liste_res = []
    liste_transaction = []
    if rUser.get(("transaction." + nom)) is not None:
        for j in range(len(json.loads(rUser.get(("transaction." + nom))))):
            liste_transaction.append(json.loads(rUser.get(("transaction." + nom)))[j])
    liste_transaction = list(set(liste_transaction))

    for j in range(len(liste_transaction)):
        liste_res.append(dict(donneur=rTransaction.get("transaction." + str(liste_transaction[j]) + ".donneur"),
                              receveur=rTransaction.get("transaction." + str(liste_transaction[j]) + ".receveur"),
                              valeur=rTransaction.get("transaction." + str(liste_transaction[j]) + ".valeur"),
                              date=rTransaction.get("transaction." + str(liste_transaction[j]) + ".date")))
    return liste_res, 200


@app.route("/chargerDonnees", methods=['GET'])
def charger_donnees():
    """
        Permet de charger les données dans la base de données

        :return: Un JSON contenant le message de confirmation
    """
    # curl -X GET http://localhost:5000/chargerDonnees

    if len(get_all_users()) == 0 or len(get_transactions()) == 0:
        return "Les données sont déjà chargées.", 200

    date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    time_stamp = calendar.timegm(time.gmtime())

    # charger users
    rUser.set("nom.Benjamin", "Benjamin")
    rUser.set("transaction.Benjamin", json.dumps([1, time_stamp]))
    rUser.set("solde.Benjamin", 400)

    rUser.set("nom.Clement", "Clement")
    rUser.set("transaction.Clement", json.dumps([1, time_stamp]))
    rUser.set("solde.Clement", 200)

    rTransaction.set("transaction.1.donneur", "Benjamin")
    rTransaction.set("transaction.1.receveur", "Clement")
    rTransaction.set("transaction.1.valeur", 100)
    rTransaction.set("transaction.1.date", date)
    rTransaction.set("transaction.1.hash",
                     generer_hash(donneur="Benjamin", receveur="Clement", valeur=100, date=date))

    rTransaction.set("transaction." + str(time_stamp) + ".donneur", "Benjamin")
    rTransaction.set("transaction." + str(time_stamp) + ".receveur", "Clement")
    rTransaction.set("transaction." + str(time_stamp) + ".valeur", 300)
    rTransaction.set("transaction." + str(time_stamp) + ".date", date)
    rTransaction.set("transaction." + str(time_stamp) + ".hash",
                     generer_hash(donneur="Benjamin",
                                  receveur="Clement",
                                  valeur=300, date=date,
                                  hash_precedent=rTransaction.get("transaction.1.hash")))

    return "Le chargement des données à réussi.", 201


@app.route("/enregisterTransaction", methods=['POST'])
def enregistrer_transaction():
    """
        Permet d'enregistrer une transaction dans la base de données

        :return: Un JSON contenant le message de confirmation
    """
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"donneur\":\"Benjamin\", \"receveur\":\"Clement\", \"valeur\":\"100\"}" http://localhost:5000/enregisterTransaction

    if not verifier_une_transaction(get_list_transaction()[-1], get_list_transaction()[-2]):
        return "La dernière transaction n'est pas valide.", 400

    time_stamp = calendar.timegm(time.gmtime())
    date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    data = request.get_json()
    donneur = data.get("donneur")
    receveur = data.get("receveur")
    valeur = data.get("valeur")
    signature = data.get("signature")
    decoded_signature = base64.b64decode(signature.encode('utf-8'))

    user = data.get("user")
    user_public_key = rUser.get("public_key." + user)
    user_public_key = load_pem_public_key(user_public_key.encode('utf-8'))
    if rUser.get("nom." + donneur) is None:
        return "Le donneur n'existe pas.", 400
    if rUser.get("nom." + receveur) is None:
        return "Le receveur n'existe pas.", 400

    if user is None:
        return "user is None", 400
    if not verify_key(user_public_key, user + donneur + receveur + valeur, decoded_signature):
        return "verification de la clef publi a echoue", 400  # probleme de clef publique !!!

    liste_transaction_donneur = json.loads(rUser.get("transaction." + donneur))
    liste_transactin_receveur = json.loads(rUser.get("transaction." + receveur))

    # on ajoute la transaction au donneur
    liste_transaction_donneur.append(time_stamp)
    rUser.set("transaction." + donneur, json.dumps(liste_transaction_donneur))

    # on ajoute la transaction au receveur
    liste_transactin_receveur.append(time_stamp)
    rUser.set("transaction." + receveur, json.dumps(liste_transactin_receveur))

    # on ajoute la transaction
    hash_precedent = get_last_hash()
    rTransaction.set("transaction." + str(time_stamp) + ".donneur", donneur)
    rTransaction.set("transaction." + str(time_stamp) + ".receveur", receveur)
    rTransaction.set("transaction." + str(time_stamp) + ".valeur", valeur)
    rTransaction.set("transaction." + str(time_stamp) + ".date", date)
    rTransaction.set("transaction." + str(time_stamp) + ".hash",
                     generer_hash(donneur=donneur,
                                  receveur=receveur,
                                  valeur=valeur,
                                  date=date,
                                  hash_precedent=hash_precedent))

    # mise a jour du solde du donneur
    solde_donneur = int(rUser.get("solde." + donneur))
    solde_donneur = solde_donneur - int(valeur)
    rUser.set("solde." + donneur, solde_donneur)

    # mise a jour du solde du receveur
    solde_receveur = int(rUser.get("solde." + receveur))
    solde_receveur = solde_receveur + int(valeur)
    rUser.set("solde." + receveur, solde_receveur)

    return "La transaction a été enregistrée.", 200


@app.route("/getSolde", methods=['POST'])
def get_solde():
    """
        Renvoie le solde d'un utilisateur

        :return: le solde de l'utilisateur
    """
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"nom\":\"Benjamin\"}" http://localhost:5000/getSolde

    data = request.get_json()
    nom = data.get("nom")
    return rUser.get("solde." + nom), 200


@app.route("/verifierTransactions", methods=['GET'])
def verifier_transactions():
    """
        Permet de vérifier les transactions

        :return: Un JSON contenant le message de confirmation
    """
    # curl -X GET  http://localhost:5000/verifierTransactions

    liste_transaction = get_list_transaction()

    for j in range(len(liste_transaction)):
        if j == 0:
            hash_precedent = ""
        else:
            hash_precedent = rTransaction.get("transaction." + str(liste_transaction[j - 1]) + ".hash")

        calculed_hash = generer_hash(donneur=rTransaction.get("transaction." + str(liste_transaction[j]) + ".donneur"),
                                     receveur=rTransaction.get(
                                         "transaction." + str(liste_transaction[j]) + ".receveur"),
                                     valeur=rTransaction.get("transaction." + str(liste_transaction[j]) + ".valeur"),
                                     date=rTransaction.get("transaction." + str(liste_transaction[j]) + ".date"),
                                     hash_precedent=hash_precedent)

        if calculed_hash != rTransaction.get("transaction." + str(liste_transaction[j]) + ".hash"):
            return "La transaction " + str(liste_transaction[j]) + " n'est pas valide.", 400

    return "Toutes les transactions sont valides.", 200


@app.route("/register", methods=['POST'])
def register():
    """
        Permet d'enregistrer un utilisateur

        :param: nom de l'utilisateur
        :param: solde de l'utilisateur
        :param: clé publique de l'utilisateur
    :return: Un JSON contenant le message de confirmation
    """
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"nom\":\"Benjamin\", \"solde\":\"100\", \"cle_publique\":\"cle_publique\"}" http://localhost:5000/register

    data = request.get_json()
    nom = data.get('nom')
    solde = data.get('solde')
    key = data.get('cle_publique')
    if rUser.get("nom." + nom) is None:
        rUser.set("nom." + nom, nom)
        rUser.set("transaction." + nom, json.dumps([]))
        rUser.set("solde." + nom, solde)
        rUser.set("public_key." + nom, key)
        return "L'utilisateur a été enregistré.", 200
    else:
        return "L'utilisateur existe déjà.", 400


def generer_hash(donneur, receveur, valeur, date, hash_precedent=""):
    """
        Permet de générer un hash pour une transaction

        :param: donneur
        :param: receveur
        :param: valeur
        :param: date
    """
    genered_hash = hashlib.sha256(
        (donneur + receveur + str(valeur) + date + hash_precedent).encode('utf-8')).hexdigest()
    return genered_hash


def convert_public_key_to_pem(public_key):
    """
        Convertit une clé publique au format PEM
        :param public_key: clé publique
        :return: clé publique au format PEM
    """

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    return pem


def get_list_transaction():
    """
        Renvoie la liste des transactions

        :return: liste des transactions
    """
    liste_users, _ = get_all_users()
    liste_transaction = []
    for i in range(len(liste_users)):
        if rUser.get(("transaction." + liste_users[i])) is not None:
            for j in range(len(json.loads(rUser.get(("transaction." + liste_users[i]))))):
                liste_transaction.append(json.loads(rUser.get(("transaction." + liste_users[i])))[j])
    liste_transaction = list(set(liste_transaction))
    liste_transaction.sort()
    return liste_transaction


def verifier_une_transaction(transaction, last_transaction=""):
    """
        Permet de vérifier une transaction

        :param last_transaction: la transaction précédente
        :param transaction: la transaction à vérifier
        :return: True si la transaction est valide, False sinon
    """
    if last_transaction == "":
        hash_precedent = ""
    else:
        hash_precedent = rTransaction.get("transaction." + str(last_transaction) + ".hash")

    verified_hash = generer_hash(donneur=rTransaction.get("transaction." + str(transaction) + ".donneur"),
                                 receveur=rTransaction.get("transaction." + str(transaction) + ".receveur"),
                                 valeur=rTransaction.get("transaction." + str(transaction) + ".valeur"),
                                 date=rTransaction.get("transaction." + str(transaction) + ".date"),
                                 hash_precedent=hash_precedent)
    if verified_hash != rTransaction.get("transaction." + str(transaction) + ".hash"):
        return False
    return True


def get_last_hash():
    """
        Permet de renvoyer le hash de la dernière transaction

        :return: le hash de la dernière transaction
    """
    liste_transaction = get_list_transaction()
    previous_hash = rTransaction.get("transaction." + str(liste_transaction[-2]) + ".hash")
    return str(previous_hash)


def verify_key(public_key, transaction_data, signature):
    """
        Permet de vérifier une signature

        :param public_key: clé publique
        :param transaction_data: données de la transaction
        :param signature: signature
        :return: True si la signature est valide, False sinon
    """
    try:
        public_key.verify(
            signature,
            transaction_data.encode('utf-8'),  # Assurez-vous que les données sont encodées en bytes
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("Verification failed:", e)
        return e


"""
    Permet de charger les données dans la base de données
"""
charger_donnees()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)