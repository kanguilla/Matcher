import pymongo
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tofriends"]
mycol = mydb["spinUsers"]

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
times = ["m", "a", "e"]
timeWeights = [0.2, 0.3, 0.5]
groupSizes = [2, 3]
groupSizeWeights = [0.75, 0.25]

x = mycol.delete_many({})
print(x.deleted_count, "documents deleted.")

size = 20
entries = []
for x in range(size):
    available = []
    blocks = []
    for k in range(random.randrange(0, 3)):
        available.append({"day": random.choice(days), "time": random.choices(times, timeWeights).pop()})
    for k in range(random.randrange(0, 2)):
        if random.randrange(100) < 50:
            blocks.append(random.choice(range(size)))
    group = random.choices(groupSizes, groupSizeWeights).pop()

    entry = {"_id": x, "confirmed": True,
             "available": available, "groupSize": group, "blackList": blocks}
    print(entry)
    entries.append(entry)
mycol.insert_many(entries)
