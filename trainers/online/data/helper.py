#!/usr/bin/env python3

from pathlib import Path
import json

def load_data():

    descriptions, categories = [], []
    runtime = Path(__file__).parent.parent.parent / 'models' / 'runtime.json'

    if not runtime.exists():
        return descriptions, categories

    with open(runtime, 'r', encoding='utf-8') as f_runtime:
        for e in json.load(f_runtime):
            if not e.get('completed', False):
                for name in e.get('data'):
                    data = Path(__file__).parent / 'data' / name
                    with open(data, 'r', encoding='utf-8') as f_data:
                        for t in json.load(f_data):
                            descriptions.append(t['Description'].strip().lower())
                            categories.append(t['Category'].strip())

    return descriptions, categories

def save_data(category, amount, description):

    folder = Path(__file__).parent
    files = list(folder.glob('part_*.json'))
    
    if not files:
        file = folder / 'part_1.json'
        buffer = []
    else:
        files.sort(key=lambda x: int(x.stem.split('_')[1]))
        file = files[-1]

        with open(file, 'r', encoding='utf-8') as f:
            buffer = json.load(f)
        
        if len(buffer) >= 100:
            number = int(file.stem.split('_')[1])
            file = folder / f'part_{number + 1}.json'
            buffer = []
    
    buffer.append(dict(
        Category=category,
        Amount=int(amount),
        Description=description
    ))
    
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(buffer, f, indent=4)