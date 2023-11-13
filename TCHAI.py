from flask import Flask
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



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
