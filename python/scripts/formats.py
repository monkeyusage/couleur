import os

file_endings = {}

for root, dirs, files in os.walk(r"data\img"):
    for file in files:
        path = os.path.join(root, file)
        ending = path.split(".")[-1]
        if ending not in file_endings.keys():
            file_endings[ending] = 1
        else:
            file_endings[ending] += 1

print(file_endings)
