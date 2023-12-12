import redis
import random
import json

rUser = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
rTransaction = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

listeTransaction = rTransaction.keys("transaction.*")

transaction = random.choice(list(listeTransaction))
for i in rTransaction.keys("transaction." + transaction.split(".")[1] + ".*"):
    rTransaction.delete(i)

for i in rUser.keys("transaction.*"):
    tmp = json.loads(rUser.get(i))
    if int(transaction.split(".")[1]) in tmp:
        tmp.remove(int(transaction.split(".")[1]))
        rUser.set(i, json.dumps(tmp))

print("Transaction " + transaction.split(".")[1] + " supprimée")
