import os
import pickle
import shutil
from pathlib import Path

def resolve(type):

    number = 1
    base_folder = Path(__file__).parent
    numbers = []
    
    for f in base_folder.iterdir():
        if f.is_dir() and f.name.startswith("version_"):
            try:
                numbers.append(int(f.name.split("_")[1]))
            except (IndexError, ValueError):
                continue
    if numbers:
        number = max(numbers)

    if type == "save":
        current_folder = base_folder / f"version_{number}"
        if current_folder.exists():
            number += 1
        new_folder = base_folder / f"version_{number}"
        os.makedirs(new_folder, exist_ok=True)
        folder_to_return = new_folder
    else:  # load
        folder_to_return = base_folder / f"version_{number}"

    version = f"version_{number}"
    return version, folder_to_return

def mark(version):

    runtime = Path(__file__).parent.parent.parent / "models" / "runtime.json"

    if not runtime.exists():
        return

    with open(runtime, "r", encoding="utf-8") as f:
        usage = json.load(f)

    for entry in usage:
        if entry["version"] == version:
            entry["completed"] = True

    with open(runtime, "w", encoding="utf-8") as f:
        json.dump(usage, f, indent=4)

def queue():

    runtime = Path(__file__).parent / "runtime.json"

    if runtime.exists():
        with open(runtime, "r", encoding="utf-8") as f:
            usage = json.load(f)
    else:
        usage = []
    
    used_files = set()
    for entry in usage:
        used_files.update(entry.get("data", []))

    folder = Path(__file__).parent.parent / "trainers" / "online" / "data"
    files = sorted(folder.glob("part_*.json"), key=lambda x: int(x.stem.split("_")[1]))
    
    files_to_use = []
    for f in files:
        if f.name in used_files:
            continue
        with open(f, "r", encoding="utf-8") as jf:
            data = json.load(jf)
        if len(data) >= 100:
            files_to_use.append(f.name)

    if not files_to_use:
        return
    
    version, folder = resolve("save")

    usage.append(dict(
        version=version,
        data=files_to_use,
        completed=False
    ))

    with open(runtime, "w", encoding="utf-8") as f:
        json.dump(usage, f, indent=4)
    
    print(f"Success: Queued new model {version} as primary model.")

def load():

    version, folder = resolve('load')
    
    if not folder.exists():
        print(f"Error: Requested version {version} not found at {folder}.")
        return
    
    with open(folder / "model.pkl", "rb") as f:
        model = pickle.load(f)
    with open(folder / "vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open(folder / "encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
    
    print(f"Success: Deployed model {version} as primary model.")
    return version, model, vectorizer, encoder

def save(model, vectorizer, encoder):

    version, folder = resolve('save')
    
    with open(folder / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(folder / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(folder / "encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)
    
    print(f"Success: Created new model {version} as primary model.")

def rollback():

    version, folder = resolve('load')

    if not folder.exists():
        print(f"Warning: Skipped model rollback as no previous version exists.")
        return
    
    shutil.rmtree(folder)

    runtime = Path(__file__).parent.parent / "runtime.json"

    if runtime.exists():
        with open(runtime, "r", encoding="utf-8") as f:
            usage = json.load(f)

        usage = [entry for entry in usage if entry.get("version") != version]

        with open(runtime, "w", encoding="utf-8") as f:
            json.dump(usage, f, indent=4)
        
    print(f"Success: Deleted old model {version} as primary model.")