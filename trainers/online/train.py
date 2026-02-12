# Step 1: Resolve model version
from models.helper import resolve

version, folder = resolve('load')

if version != "version_1":

    # Step 2: Load existing model, vectorizer, encoder
    from models.helper import load as load_model
    version, model, vectorizer, encoder = load_model()

    # Step 3: Load only new online data that hasn't been used yet
    from .helper import load as load_online_data
    descriptions, categories = load_online_data()

    if not descriptions:
        print("No new online data to train on.")
        exit()

    print(f"Incremental training on {len(descriptions)} new samples.")

    # Step 4: Transform new data using existing vectorizer and encoder
    X_new = vectorizer.transform(descriptions)

    from sklearn.preprocessing import LabelEncoder
    y_new = encoder.transform(categories)

    # Step 5: Incremental training
    from sklearn.linear_model import SGDClassifier
    import numpy as np

    if not hasattr(model, "classes_"):
        # First partial_fit
        model.partial_fit(X_new, y_new, classes=np.unique(y_new))
    else:
        model.partial_fit(X_new, y_new)

    # Step 6: Save updated model
    from models.helper import save
    save(model, vectorizer, encoder)

    # Step 7: Mark runtime.json as completed for these files
    from models.helper import mark
    mark(version)

    print(f"Successfully updated model {version} with {len(descriptions)} new samples.")

else:
    print(f"Warning: Skipped online retraining as no older version exists.")