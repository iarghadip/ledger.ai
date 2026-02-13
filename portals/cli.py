#!/usr/bin/env python3

import sys
from models.helper import run_model

try:
    while True:
        
        query = input('Enter Description: ')
            
        version, category = run_model(query)
        
        print(f'\n{version}: {category}\n')

except KeyboardInterrupt:
    sys.exit(0)