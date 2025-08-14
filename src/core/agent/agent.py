from __future__ import annotations
import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from ... import env as _env  # Load environment variables  # noqa: F401
from .kb import kb_search
from .response_templates import RAG_SYSTEM_PROMPT


MODEL = os.getenv("MODEL", "gpt-4o-mini")

model = OpenAIModel(MODEL)

agent = Agent(model, tools=[kb_search], system_prompt=RAG_SYSTEM_PROMPT)

__all__ = ["agent", "kb_search"]
