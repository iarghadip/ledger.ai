#!/usr/bin/env python3

import os
import json
import pickle
import shutil
from pathlib import Path

def print_deployed(silent=False):
	
	version, _ = resolve_deployed('load')
	
	if version == 'version_0':
		print(f'Warning: No model is currently deployed.')
	elif not silent:
		print(f'Success: Deployed model {version} as primary model.')

def resolve_deployed(type, create=True):
	
	number = 0
	
	for v in Path(__file__).parent.iterdir():
		if v.is_dir() and v.name.startswith('version_'):
			try:
				current = int(v.name.split('_')[1])
				if current > number:
					number = current
			except (IndexError, ValueError):
				continue
	
	if type == 'save':
		number += 1
	
	version = f'version_{number}'
	folder = Path(__file__).parent / version
	if type == 'save' and create: os.makedirs(folder, exist_ok=True)

	return version, folder

def complete_version(version):
	
	runtime = Path(__file__).parent / 'runtime.json'

	with open(runtime, 'r', encoding='utf-8') as f_runtime:
		
		usage = json.load(f_runtime)
		
		for entry in usage:
			if entry['version'] == version:
				entry['completed'] = True
		
		with open(runtime, 'w', encoding='utf-8') as f_runtime:
			json.dump(usage, f_runtime, indent=4)

def create_version():
	
	runtime = Path(__file__).parent / 'runtime.json'
	
	with open(runtime, 'r', encoding='utf-8') as f_runtime:
		
		usage = json.load(f_runtime)

		if any(e.get('completed') is False for e in usage):
			print('Warning: Skipped model queue as a previous version not yet executed.')
			return
		
		used_files = set()
		
		for entry in usage:
			used_files.update(entry.get('data', []))
			
		folder = Path(__file__).parent.parent / 'trainers' / 'online' / 'data'
		files = sorted(folder.glob('part_*.json'), key=lambda x: int(x.stem.split('_')[1]))
		files_to_use = []
		
		for f in files:
			if f.name in used_files:
				continue
			with open(f, 'r', encoding='utf-8') as jf:
				data = json.load(jf)
			if len(data) >= 100:
				files_to_use.append(f.name)
				
		if not files_to_use:
			return
		
		version, folder = resolve_deployed('save', False)
		
		usage.append(dict(
			version=version,
			data=files_to_use,
			completed=False
		))
		
		with open(runtime, 'w', encoding='utf-8') as f:
			json.dump(usage, f, indent=4)
			
		print(f'Success: Queued new model {version} as primary model.')

def create_model(model, vectorizer, encoder):
	
	version, folder = resolve_deployed('save')
	
	with open(folder / 'model.pkl', 'wb') as f:
		pickle.dump(model, f)
	with open(folder / 'vectorizer.pkl', 'wb') as f:
		pickle.dump(vectorizer, f)
	with open(folder / 'encoder.pkl', 'wb') as f:
		pickle.dump(encoder, f)
	
	complete_version(version)
		
	print(f'Success: Created new model {version} for deployement.')
	print_deployed()

def load_model():
	
	version, folder = resolve_deployed('load')
	
	print_deployed(silent=True)
	
	if folder.exists():
		
		with open(folder / 'model.pkl', 'rb') as f:
			model = pickle.load(f)
		with open(folder / 'vectorizer.pkl', 'rb') as f:
			vectorizer = pickle.load(f)
		with open(folder / 'encoder.pkl', 'rb') as f:
			encoder = pickle.load(f)
			
		return version, model, vectorizer, encoder

def revert_model():

    version, folder = resolve_deployed('load')
    
    if not folder.exists():
        print(f'Warning: Skipped model rollback as no model is currently deployed.')
        return

    shutil.rmtree(folder)
    
    runtime = Path(__file__).parent / 'runtime.json'
    
    if runtime.exists():
        with open(runtime, 'r', encoding='utf-8') as f:
            usage = json.load(f)

        usage = [entry for entry in usage if entry.get('version') != version]
        
        with open(runtime, 'w', encoding='utf-8') as f:
            json.dump(usage, f, indent=4)
    
    print(f'Success: Reverted model {version} and removed entry from runtime.')
    
    if 'print_deployed' in globals():
        print_deployed()

def run_model(query):
	version, model, vectorizer, encoder = load_model()
	X_new = vectorizer.transform([query])
	pred = model.predict(X_new)
	return version, str(encoder.inverse_transform(pred)[0])