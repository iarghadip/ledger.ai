from models.helper import resolve

version, folder = resolve('load')

if version == "version_1":

    from .data.helper import load
    from sklearn.preprocessing import LabelEncoder

    categories, descriptions = load()

    encoder = LabelEncoder()
    y = encoder.fit_transform(categories)

    print(y)

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=None,
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform(descriptions)

    print(X.shape)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    from sklearn.linear_model import SGDClassifier

    # Use SGDClassifier with log loss (like logistic regression) for incremental learning
    model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3)
    model.fit(X_train, y_train)

    from sklearn.metrics import accuracy_score

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy)

    from models.helper import save
    
    save(model, vectorizer, encoder)

    # # Optional: Inspect top features
    # import numpy as np
    # feature_names = vectorizer.get_feature_names_out()
    # class_labels = model.classes_
    #
    # if len(class_labels) == 2:
    #     coefficients = model.coef_[0]
    #
    #     top_positive = np.argsort(coefficients)[-10:]
    #     top_negative = np.argsort(coefficients)[:10]
    #
    #     for i in top_positive:
    #         pass
    #     for i in top_negative:
    #         pass
    #
    # else:
    #     for i, class_label in enumerate(class_labels):
    #         class_coefficients = model.coef_[i]
    #         top_indices = np.argsort(class_coefficients)[-10:][::-1]
    #         pass

else:
    print(f"Warning: Skipped model retraining as a newer version {version} already exists.")