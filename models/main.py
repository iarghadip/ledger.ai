import pickle
import os

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def save(model, vectorizer, label_encoder, folder=MODEL_DIR):
    with open(f"{folder}/model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open(f"{folder}/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    
    with open(f"{folder}/label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)
    
    print(f"Saved model, vectorizer, and label encoder to '{folder}/' folder.")

def load(folder=MODEL_DIR):
    with open(f"{folder}/model.pkl", "rb") as f:
        model = pickle.load(f)
    
    with open(f"{folder}/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    
    with open(f"{folder}/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    
    return model, vectorizer, label_encoder