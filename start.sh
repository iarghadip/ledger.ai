pip install -r requirements.txt
uvicorn api:app --host $(hostname -I) --port 8001 --reload