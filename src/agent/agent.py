from __future__ import annotations
import os
from .. import env  # load .env
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import SystemPrompt
from .kb import kb_search
from .response_templates import RAG_SYSTEM_PROMPT


MODEL = os.getenv("MODEL", "gpt-4o-mini")

system = SystemPrompt(RAG_SYSTEM_PROMPT)

model = OpenAIModel(MODEL)

agent = Agent(model, tools=[kb_search], system_prompt=system)


__all__ = ["agent", "kb_search"]
