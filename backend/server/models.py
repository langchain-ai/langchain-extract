import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI

for provider in ["OPENAI_API_KEY", "TOGETHER_API_KEY", "FIREWORKS_API_KEY"]:
    if provider not in os.environ:
        os.environ[provider] = "placeholder"

SUPPORTED_MODELS = {
    "gpt-3.5-turbo": ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    "gpt-4-0125-preview": ChatOpenAI(model="gpt-4-0125-preview", temperature=0),
    "fireworks": ChatFireworks(model="accounts/fireworks/models/firefunction-v1"),
    "together-ai-mistral-8x7b-instruct-v0.1": ChatOpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=os.environ["TOGETHER_API_KEY"],
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    ),
}

CHUNK_SIZES = {  # in tokens, defaults to int(4_096 * 0.8). Override here.
    "gpt-4-0125-preview": int(128_000 * 0.8),
}


def get_chunk_size(model_name: str) -> int:
    """Get the chunk size."""
    return CHUNK_SIZES.get(model_name, int(4_096 * 0.8))


def get_model(model_name: Optional[str] = None) -> BaseChatModel:
    """Get the model."""
    if model_name is None:
        return SUPPORTED_MODELS["gpt-3.5-turbo"]
    else:
        supported_model_names = list(SUPPORTED_MODELS.keys())
        if model_name not in supported_model_names:
            raise ValueError(
                f"Model {model_name} not found. "
                f"Supported models: {supported_model_names}"
            )
        else:
            return SUPPORTED_MODELS[model_name]
