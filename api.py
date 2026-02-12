#!/usr/bin/env python3

from main import get_category
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import Any, Literal, Annotated

app = FastAPI()

DEVELOPER_MODE = True

class SuccessResponse(BaseModel):
    success: Literal[True] = True
    message: str | None = None
    body: Any | None = None

class ErrorResponse(BaseModel):
    success: Literal[False] = False
    message: str | None
    body: Any | None = None
    @field_validator('message')
    @classmethod
    def prepend_error_tag(cls, v: str | None) -> str | None:
        if v is not None and not v.startswith("Error: "):
            return f"Error: {v}"
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors() if DEVELOPER_MODE else None
    
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            message="Could not validate request inputs.", 
            body=error_details
        ).model_dump(exclude_none=True), 
    )

@app.get("/", response_model=SuccessResponse | ErrorResponse, response_model_exclude_none=True)
def read_root(
    query: Annotated[str, Query(min_length=5, max_length=30)]
):
    category = get_category(query)
    return SuccessResponse(
        body={
            "description": query,
            "category": category
        }
    )