import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI


def get_supported_models():
    """Get models according to environment secrets."""
    models = {}
    if "OPENAI_API_KEY" in os.environ:
        models["gpt-3.5-turbo"] = {
            "chat_model": ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            "description": "GPT-3.5 Turbo",
        }
        if os.environ.get("DISABLE_GPT4").lower() != "true":
            models["gpt-4-0125-preview"] = {
                "chat_model": ChatOpenAI(model="gpt-4-0125-preview", temperature=0),
                "description": "GPT-4 0125 Preview",
            }
    if "FIREWORKS_API_KEY" in os.environ:
        models["fireworks"] = {
            "chat_model": ChatFireworks(
                model="accounts/fireworks/models/firefunction-v1",
                temperature=0,
            ),
            "description": "Fireworks Firefunction-v1",
        }
    if "TOGETHER_API_KEY" in os.environ:
        models["together-ai-mistral-8x7b-instruct-v0.1"] = {
            "chat_model": ChatOpenAI(
                base_url="https://api.together.xyz/v1",
                api_key=os.environ["TOGETHER_API_KEY"],
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                temperature=0,
            ),
            "description": "Mixtral 8x7B Instruct v0.1 (Together AI)",
        }

    return models


SUPPORTED_MODELS = get_supported_models()
DEFAULT_MODEL = "gpt-3.5-turbo"


CHUNK_SIZES = {  # in tokens, defaults to int(4_096 * 0.8). Override here.
    "gpt-4-0125-preview": int(128_000 * 0.8),
}


def get_chunk_size(model_name: str) -> int:
    """Get the chunk size."""
    return CHUNK_SIZES.get(model_name, int(4_096 * 0.8))


def get_model(model_name: Optional[str] = None) -> BaseChatModel:
    """Get the model."""
    if model_name is None:
        return SUPPORTED_MODELS[DEFAULT_MODEL]["chat_model"]
    else:
        supported_model_names = list(SUPPORTED_MODELS.keys())
        if model_name not in supported_model_names:
            raise ValueError(
                f"Model {model_name} not found. "
                f"Supported models: {supported_model_names}"
            )
        else:
            return SUPPORTED_MODELS[model_name]["chat_model"]
