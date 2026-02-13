#!/usr/bin/env python3

import sys
from models.helper import run_model
from trainers.online.data.helper import save_data

print('Type down your transaction description.\n')
print('f) Provide Feedback')
print('q) Quit CLI Portal\n')

try:
    while True:
        
        query = input('Enter Query: ').lower()

        if query == 'q':
            sys.exit(0)
        
        if query == 'f':
            category = input('Enter Category: ')
            amount = input('Enter Amount: ')
            description = input('Enter Description: ')
            save_data(category, amount, description)
        
        version, category = run_model(query)
        
        print(f'\n{version}: {category}\n')

except KeyboardInterrupt:
    sys.exit(0)