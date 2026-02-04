from main import get_category
from fastapi import FastAPI

app = FastAPI()

def get_response(success: bool = True, message: str | None = None, body: dict = {}):
    response = {"success": success}
    if message: response["message"] = message
    if body: response["body"] = body
    return response

@app.get("/")
def read_root(query: str | None = None):
    if query and query.strip():
        category = get_category(query)
        return get_response(body={
            "description": query,
            "category": category
        })
    else:
        return get_response(success=False, message="Query was not provided.")