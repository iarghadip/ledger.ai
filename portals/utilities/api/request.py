#!/usr/bin/env python3

from .response import ErrorResponse
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=400,
		content=ErrorResponse(
			message='Could not validate request inputs.',
			body=exc.errors()
		).model_dump(exclude_none=True),
	)