#!/usr/bin/env python3

from pydantic import BaseModel, field_validator
from typing import Any, Literal

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
		if v is not None and not v.startswith('Error: '):
			return f'Error: {v}'
		return v