import pickle
import os
from pathlib import Path
from models.helper import resolve

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

    version, folder = resolve('load')

    if version != "version_1":
        print(f"Warning: Skipped model retraining as a newer version {version} already exists.")
        return
    
    os.makedirs(folder, exist_ok=True)
    
    with open(folder / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(folder / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(folder / "encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)
    
    print(f"Success: Created new model version_1 as primary model.")