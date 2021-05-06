import os

os.mkdir("data/transforms")
for folder in os.listdir("data/img"):
    os.mkdir(f"data/transforms/{folder}")
