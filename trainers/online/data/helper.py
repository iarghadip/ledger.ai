from pathlib import Path
import json

def load():

    descriptions = []
    categories = []

    folder = Path(__file__).parent.parent.parent / "models" / "runtime.json"

    if not folder.exists():
        return descriptions, categories

    with open(folder, "r", encoding="utf-8") as f:
        runtime = json.load(f)
    
    next_entry = None
    for entry in runtime:
        if not entry.get("completed", False):
            next_entry = entry
            break

    if not next_entry:
        return descriptions, categories

    folder = Path(__file__).parent
    for file_name in next_entry["data"]:
        file_path = folder / file_name
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            for x in json.load(f):
                descriptions.append(x["Description"].strip().lower())
                categories.append(x["Category"].strip())

    return descriptions, categories

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
