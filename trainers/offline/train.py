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

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

from .persistence import save

save(model, vectorizer, encoder)

import pandas as pd
import numpy as np

feature_names = vectorizer.get_feature_names_out()

class_labels = model.classes_

if len(class_labels) == 2:
    coefficients = model.coef_[0]

    top_positive = np.argsort(coefficients)[-10:]
    top_negative = np.argsort(coefficients)[:10]
    
    #print(f"\n--- Top indicators for '{class_labels[1]}' (Positive Class) ---")
    for i in top_positive:
        pass
        #print(f"{feature_names[i]}: {coefficients[i]:.4f}")
        
    #print(f"\n--- Top indicators for '{class_labels[0]}' (Negative Class) ---")
    for i in top_negative:
        pass
        #print(f"{feature_names[i]}: {coefficients[i]:.4f}")

else:
    #print("\n--- Top 10 Keywords per Category ---")
    for i, class_label in enumerate(class_labels):
        
        class_coefficients = model.coef_[i]
        
        top_indices = np.argsort(class_coefficients)[-10:][::-1]
        
        #print(f"\nCategory: {class_label}")
        #for idx in top_indices:
            #print(f"  {feature_names[idx]} ({class_coefficients[idx]:.4f})")