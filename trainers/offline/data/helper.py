#!/usr/bin/env python3

from pathlib import Path
import json

def load_data():

    descriptions, categories = [], []

    for data in Path(__file__).parent.glob('*.json'):
        with open(data, 'r', encoding='utf-8') as f_data:
            for t in json.load(f_data):
                descriptions.append(t['Description'].strip().lower())
                categories.append(t['Category'].strip())

    return descriptions, categories