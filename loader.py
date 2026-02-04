import json

descriptions = []
categories = []

with open("data.json", "r", encoding="utf-8") as f:
    for x in json.load(f):
        descriptions.append(x["Description"].strip().lower())
        categories.append(x["Category"].strip())