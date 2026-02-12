#!/usr/bin/env python3

from models.helper import resolve_deployed

version, _ = resolve_deployed('load')

if version == 'version_0':
    
    from .data.helper import load
    from sklearn.preprocessing import LabelEncoder

    categories, descriptions = load()

    encoder = LabelEncoder()
    y = encoder.fit_transform(categories)

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=None,
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform(descriptions)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    from sklearn.linear_model import SGDClassifier
    
    model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3)
    model.fit(X_train, y_train)

    from models.helper import create_model
    
    create_model(model, vectorizer, encoder)

else:
    
    print(f'Warning: Skipped model training as a newer version {version} already exists.')