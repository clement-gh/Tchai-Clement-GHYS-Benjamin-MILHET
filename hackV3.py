import redis
import json
import hashlib
import datetime
import calendar
import time

rUser = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
rTransaction = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

listeTransaction = rTransaction.keys("transaction.*")
listeTransaction.sort()

last_transaction = listeTransaction[-1].split(".")[1]

donneur = "jean"
receveur = "pierre"
valeur = "1000000"
date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
hash_precedent = rTransaction.get("transaction." + last_transaction + ".hash")
hash = hashlib.sha256((donneur + receveur + valeur + date + hash_precedent).encode('utf-8')).hexdigest()
time_stamp = calendar.timegm(time.gmtime())

rTransaction.set("transaction." + str(time_stamp) + ".donneur", donneur)
rTransaction.set("transaction." + str(time_stamp) + ".receveur", receveur)
rTransaction.set("transaction." + str(time_stamp) + ".valeur", valeur)
rTransaction.set("transaction." + str(time_stamp) + ".date", date)
rTransaction.set("transaction." + str(time_stamp) + ".hash", hash)

if rUser.get("nom." + donneur) is None:
    rUser.set("nom." + donneur, donneur)
    rUser.set("transaction." + donneur, json.dumps([str(time_stamp)]))
    rUser.set("solde." + donneur, "1000000")
else:
    tmp = json.loads(rUser.get("transaction." + donneur))
    tmp.append(str(time_stamp))
    rUser.set("transaction." + donneur, json.dumps(tmp))
    solde_donneur = int(rUser.get("solde." + donneur))
    solde_donneur = solde_donneur + int(valeur)
    rUser.set("solde." + donneur, str(solde_donneur))

if rUser.get("nom." + receveur) is None:
    rUser.set("nom." + receveur, receveur)
    rUser.set("transaction." + receveur, json.dumps([str(time_stamp)]))
    rUser.set("solde." + receveur, "-1000000")
else:
    tmp = json.loads(rUser.get("transaction." + receveur))
    tmp.append(str(time_stamp))
    rUser.set("transaction." + receveur, json.dumps(tmp))
    solde_receveur = int(rUser.get("solde." + receveur))
    solde_receveur = solde_receveur - int(valeur)
    rUser.set("solde." + receveur, str(solde_receveur))



