import calendar
import time
from flask import Flask, request
import sys
import redis
import json
import hashlib

from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})

rUser = redis.Redis(host='TCHAI_redis', port=6379, db=0, decode_responses=True)
rTransaction = redis.Redis(host='TCHAI_redis', port=6379, db=1, decode_responses=True)


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/getTransactions", methods=['GET'])
def get_transactions():
    """
        Renvoie la liste des transactions

        :return: liste des transactions
    """
    # curl -X GET  http://127.0.0.1:5000/getTransactions

    liste_res = []
    tmp = rTransaction.keys("transaction.*")
    tmp.sort()
    list_id = []
    list_data = []
    for i in range(len(tmp)):
        list_id.append(tmp[i].split(".")[1])
        list_data.append(tmp[i].split(".")[2])

    list_id = list(set(list_id))
    list_data = list(set(list_data))

    for i in range(len(list_id)):
        liste_res.append({})
        for j in range(len(list_data)):
            liste_res[i][list_data[j]] = rTransaction.get("transaction." + list_id[i] + "." + list_data[j])

    return liste_res

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
    list_id_transaction = json.loads(rUser.get("transaction." + nom))
    for i in range(len(list_id_transaction)):
        #liste_res.append(list_id_transaction[i])
        #liste_res.append({})
        liste_res[i].append(rTransaction.get("transaction.1.donneur"))
        #liste_res[i]["donneur"] = rTransaction.get("transaction." + list_id_transaction[i] + ".donneur")
        #liste_res[i]["receveur"] = rTransaction.get("transaction." + list_id_transaction[i] + ".receveur")
        #liste_res[i]["valeur"] = rTransaction.get("transaction." + list_id_transaction[i] + ".valeur")
    return liste_res

@app.route("/chargerDonnees", methods=['GET'])
def charger_donnees():
    """
        Permet de charger les données dans la base de données

        :return: Un JSON contenant le message de confirmation
    """
    # curl -X GET http://localhost:5000/chargerDonnees

    # charger users
    rUser.set("nom.Benjamin", "Benjamin")
    rUser.set("transaction.Benjamin", json.dumps([1, 2]))
    rUser.set("solde.Benjamin", "400")

    rUser.set("nom.Clement", "Clement")
    rUser.set("transaction.Clement", json.dumps([1, 2]))
    rUser.set("solde.Clement", "200")


    rTransaction.set("transaction.1.donneur", "Benjamin")
    rTransaction.set("transaction.1.receveur", "Clement")
    rTransaction.set("transaction.1.valeur", "100")

    rTransaction.set("transaction.2.donneur", "Benjamin")
    rTransaction.set("transaction.2.receveur", "Clement")
    rTransaction.set("transaction.2.valeur", "300")

    return "Le chargement des données à réussi."

@app.route("/enregisterTransaction", methods=['POST'])
def enregistrer_transaction():


    #  curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"donneur\":\"Benjamin\", \"receveur\":\"Clement\", \"valeur\":\"100\"}" http://localhost:5000/enregisterTransaction
    time_stamp = calendar.timegm(time.gmtime())

    data = request.get_json()
    donneur = data.get("donneur")
    receveur = data.get("receveur")
    valeur = data.get('valeur')



    liste_transaction_donneur= json.loads(rUser.get("transaction." + donneur))
    liste_transactin_receveur= json.loads(rUser.get("transaction." + receveur))


    #on ajoute la transaction au donneur
    liste_transaction_donneur.append(time_stamp)   
    rUser.set("transaction." + donneur, json.dumps(liste_transaction_donneur))
    
    #on ajoute la transaction au receveur
    liste_transactin_receveur.append(time_stamp)
    rUser.set("transaction." + receveur, json.dumps(liste_transactin_receveur))

    #on ajoute la transaction 
    rTransaction.set("transaction." + str(time_stamp) + ".donneur", donneur)
    rTransaction.set("transaction." + str(time_stamp) + ".receveur", receveur)
    rTransaction.set("transaction." + str(time_stamp) + ".valeur", valeur)
  
    #mise a jour du solde du donneur
    solde_donneur = int(rUser.get("solde." + donneur))
    solde_donneur = solde_donneur - int(valeur)
    rUser.set("solde." + donneur, str(solde_donneur))

    #mise a jour du solde du receveur
    solde_receveur = int(rUser.get("solde." + receveur))
    solde_receveur = solde_receveur + int(valeur)
    rUser.set("solde." + receveur, str(solde_receveur))

    

    return "La transaction a été enregistrée."


@app.route("/getSolde", methods=['GET'])
def get_solde():
    """
        Renvoie le solde d'un utilisateur

        :return: le solde de l'utilisateur
    """
    # curl -X GET  http://localhost:5000/getSolde?nom=Benjamin

    nom = request.args.get('nom')
    return rUser.get("solde." + nom)

def generer_hash(transaction):
    transaction_string = json.dumps(transaction, sort_keys=True).encode('utf-8')
    return hashlib.sha256(transaction_string).hexdigest()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            charger_donnees()
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
