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

def save(category, amount, description):

    folder = Path(__file__).parent
    files = list(folder.glob("part_*.json"))
    
    if not files:
        file = folder / "part_1.json"
        buffer = []
    else:
        files.sort(key=lambda x: int(x.stem.split('_')[1]))
        file = files[-1]

        with open(file, "r", encoding="utf-8") as f:
            buffer = json.load(f)
        
        if len(buffer) >= 100:
            number = int(file.stem.split('_')[1])
            file = folder / f"part_{number + 1}.json"
            buffer = []
    
    buffer.append(dict(
        Category=category,
        Amount=amount,
        Description=description
    ))
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(buffer, f, indent=4)
