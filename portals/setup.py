#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ledger.ai',
    version='1.0.0',
    description='Determine transaction category from transaction description.',
    author='Arghadip Das',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.95.0',
        'uvicorn>=0.22.0',
        'scikit-learn>=1.2.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'pydantic>=2.0.0',
    ],
    python_requires='>=3.8',
)

from pathlib import Path
import json

runtime = Path(__file__).parent.parent / 'models' / 'runtime.json'

if not runtime.exists():
    
    with open(runtime, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=4)

with open(runtime, 'r', encoding='utf-8') as f:
    data = json.load(f)