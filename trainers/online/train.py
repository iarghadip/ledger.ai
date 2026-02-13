#!/usr/bin/env python3

from models.helper import resolve_deployed

version, _ = resolve_deployed('load')

if version != 'version_0':
    
    from .data.helper import load_data
    
    descriptions, categories = load_data()
    
    if len(categories) >= 100:
        
        from models.helper import load_model
        
        version, model, vectorizer, encoder = load_model()
        
        X_new = vectorizer.transform(descriptions)
    
        from sklearn.preprocessing import LabelEncoder
        
        y_new = encoder.transform(categories)
        
        from sklearn.linear_model import SGDClassifier
        
        import numpy as np
    
        if not hasattr(model, 'classes_'):
            model.partial_fit(X_new, y_new, classes=np.unique(y_new))
        else:
            model.partial_fit(X_new, y_new)
        
        from models.helper import create_model
        
        create_model(model, vectorizer, encoder)
    
    else:
        
        print(f'Message: Skipped model training as not enough data exists.')

else:
    
    print(f'Message: Skipped model training as no older version exists.')