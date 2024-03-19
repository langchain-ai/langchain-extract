from __future__ import annotations

import os
from typing import Callable, Literal, NamedTuple, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI
from sqlalchemy.engine import URL


def get_postgres_url() -> URL:
    url = URL.create(
        drivername="postgresql",
        username="langchain",
        password="langchain",
        host=os.environ.get("PG_HOST", "localhost"),
        database="langchain",
        port=5432,
    )
    return url


class ChatModel(NamedTuple):
    name: str
    chunk_size: int
    constructor: Callable


SUPPORTED_MODELS = (
    ChatModel(  # Default
        name="gpt-3.5-turbo",
        chunk_size=int(4_096 * 0.8),
        constructor=lambda: ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
        ),
    ),
    ChatModel(
        name="gpt-4-0125-preview",
        chunk_size=int(128_000 * 0.8),
        constructor=lambda: ChatOpenAI(
            model="gpt-4-0125-preview",
            temperature=0,
        ),
    ),
    ChatModel(
        name="fireworks",
        chunk_size=int(4_096 * 0.8),
        constructor=lambda: ChatFireworks(
            model="accounts/fireworks/models/firefunction-v1"
        ),
    ),
    ChatModel(
        name="together-ai-mistral-8x7b-instruct-v0.1",
        chunk_size=int(4_096 * 0.8),
        constructor = lambda: ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.environ["TOGETHER_API_KEY"],
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        )
    ),
)
ModelNameLiteral = Literal[
    "gpt-3.5-turbo",
    "gpt-4-0125-preview",
    "fireworks",
    "together-ai-mistral-8x7b-instruct-v0.1",
]


def get_model(model_name: Optional[str] = None) -> BaseChatModel:
    """Get the model."""
    if model_name is None:
        model = SUPPORTED_MODELS[0]
    else:
        supported_model_names = [model.name for model in SUPPORTED_MODELS]
        if model_name not in supported_model_names:
            raise ValueError(
                f"Model {model_name} not found. Supported models: {supported_model_names}"
            )
        else:
            model = next(
                model for model in SUPPORTED_MODELS if model.name == model_name
            )
    return model
