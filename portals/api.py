#!/usr/bin/env python3

from models.helper import run_model
from .utilities.api.response import SuccessResponse, ErrorResponse
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from .utilities.api.request import validation_exception_handler

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get('/', response_model=SuccessResponse | ErrorResponse, response_model_exclude_none=True)
def read_root(
	query: Annotated[str, Query(min_length=5, max_length=30)]
):
	version, category = run_model(query)
	return SuccessResponse(
		body=dict(
			version=version,
			description=query,
			category=str(category)
		)
	)