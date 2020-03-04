import json
import random
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tofriends"]
mycol = mydb["spinUsers"]

population = []
for e in mycol.find({"available": {"$elemMatch": {"day": "thursday"}}}):
    population.append(e)


# for e in mycol.find():
#     population.append(e)

def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses


def genset(people):
    random.shuffle(people)

    twos, threes = partition(lambda p: p["groupSize"] == 2, people)
    average = 0
    matches = []
    length = len(people)

    while len(threes) > 0:
        a = threes.pop()
        if len(threes) > 0:
            b = threes.pop()
            score = (compat(a, b))
            average += score
            if len(threes) > 0:
                c = threes.pop()
                score += (compat(a, c))
                score += (compat(b, c))
                score = score / 3
                average += score
                matches.append({"score": score, "members": [a["_id"], b["_id"], c["_id"]]})
            else:
                matches.append({"score": score, "members": [a["_id"], b["_id"]]})
        else:
            twos.append(a)

    while len(twos) > 0:
        a = twos.pop()
        if len(twos) > 0:
            b = twos.pop()
            score = (compat(a, b))
            average += score
            matches.append({"score": score, "members": [a["_id"], b["_id"]]})

    return {"matches": matches, "average": average / length}


def compat(x, y):
    distance = 0
    distance += abs(x["groupSize"] - y["groupSize"])
    distance += 0 if set(map(lambda l: (json.dumps(l)), x["available"])) & set(
        map(lambda l: (json.dumps(l)), y["available"])) else 1
    distance += 100 if set(map(lambda l: (json.dumps(l)), x["blackList"])) & set(
        map(lambda l: (json.dumps(l)), y["blackList"])) else 0
    return distance


print("Total " + str(len(population)) + " people")
for entry in population:
    print(entry)

scores = []
best = {"average": 10000}
d = 1000
print("Running " + str(d) + " rounds...")
for i in range(d):
    k = genset(population.copy())
    scores.append(k["average"])
    if k["average"] < best["average"]:
        best = k

print("Best result:")
print(json.dumps(best, indent=4, sort_keys=True))
