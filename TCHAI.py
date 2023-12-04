from flask import Flask, request, jsonify, Response
import sys
import redis
import json

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
def getTransactions():
    """
        Renvoie la liste des transactions

        :return: liste des transactions
    """
    # curl -X GET  http://127.0.0.1:5000/getTransactions

    liste_res = []
    tmp = rTransaction.keys("transaction.*.*")
    tmp.sort()
    for i in range(len(tmp)):
        liste_res.append(rTransaction.get(tmp[i]))

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


    # charger tweets
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

    data = request.get_json()
    donneur = data.get("donneur")
    receveur = data.get("receveur")
    valeur = data.get('valeur')
 


    #on ajoute la transaction 
    rTransaction.set("transaction." + str(rTransaction.dbsize()+1) + ".donneur", donneur)
    rTransaction.set("transaction." + str(rTransaction.dbsize()+1) + ".receveur", receveur)
    rTransaction.set("transaction." + str(rTransaction.dbsize() +1) + ".valeur", valeur)
    
    
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

    








    

    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
