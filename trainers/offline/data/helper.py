#!/usr/bin/env python3

from pathlib import Path
import json

def load():

    descriptions = []
    categories = []

    for file in Path(__file__).parent.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            for x in json.load(f):
                descriptions.append(x["Description"].strip().lower())
                categories.append(x["Category"].strip())

    return descriptions, categories