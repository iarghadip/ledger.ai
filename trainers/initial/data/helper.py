from pathlib import Path
import json

def load():

    buffer = dict(
        descriptions=[], 
        categories=[]
    )

    for file in Path(__file__).parent.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            for x in json.load(f):
                buffer['descriptions']
                    .append(x["Description"].strip().lower())
                buffer['categories']
                    .append(x["Category"].strip())

    return buffer