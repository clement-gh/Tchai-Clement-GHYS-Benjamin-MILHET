import redis

rTransaction = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

print(rTransaction.keys("transaction.*.valeur"))

for i in rTransaction.keys("transaction.*.valeur"):
    rTransaction.set(i, int(rTransaction.get(i)) * 100)
    print(rTransaction.get(i))