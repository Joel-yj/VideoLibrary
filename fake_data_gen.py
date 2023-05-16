from mimesis import Generic
import json

generic = Generic()
data = []

# Generates 1mil fake data
for _ in range(10):
    record = {
        "videoPath": generic.random.choice(["videos/test1.mp4","videos/test2.mp4","videos/test3.mp4","videos/test4.mp4"]),
        "age": generic.random.randint(18, 90),
        "isCarryingBackpack": generic.random.choice(["true","false"]),
        "isCarryingBag": generic.random.choice(["true","false"]),
        "lowerBodyClothing": generic.random.choice(["jeans", "skirt", "shorts", "pants"]),
        "lenLowerBodyClothing": generic.random.choice(["short", "medium", "long"]),
        "sleeveLength": generic.random.choice(["short", "medium", "long"]),
        "hairLength": generic.random.choice(["bald", "short", "medium", "long"]),
        "isWearingHat": generic.random.choice(["true","false"]),
        "gender": generic.random.choice(["M", "F"]),
        "colorUpperBodyClothing": generic.random.choice(['Blue','Red','White','Green']),
        "colorLowerBodyClothing": generic.random.choice(['Blue','Red','White','Green']),
    }
    data.append(record)

with open('database/azuretest.json', 'w') as f:
    json.dump(data, f)