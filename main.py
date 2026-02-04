from models.main import load

model, vectorizer, label_encoder = load()

def get_category(query):
    X_new = vectorizer.transform([query])
    pred = model.predict(X_new)
    return label_encoder.inverse_transform(pred)[0]

if __name__ == "__main__":
    while True:
        query = input('Enter description: ')
        category = get_category(query)
        print(category)