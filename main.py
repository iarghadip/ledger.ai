from models.main import load

model, vectorizer, label_encoder = load()

while True:
    test_text = [input('Enter description: ')]
    if not test_text[0].strip():
        break

    X_new = vectorizer.transform(test_text)
    pred = model.predict(X_new)

    print(label_encoder.inverse_transform(pred))