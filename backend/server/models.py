import os
from typing import Literal, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI

SUPPORTED_MODELS = {
    "gpt-3.5-turbo": ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    "gpt-4-0125-preview": ChatOpenAI(model="gpt-4-0125-preview", temperature=0),
    "fireworks": ChatFireworks(model="accounts/fireworks/models/firefunction-v1"),
    "together-ai-mistral-8x7b-instruct-v0.1": ChatOpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=os.environ["TOGETHER_API_KEY"],
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    ),

def get_supported_models(): 
   models = {}
   if 'OPENAI_API_KEY' in env: 
      models['gpt-3.5-turbo'] = ChatOpenAI()..
    if ... in os.environ:
      models[...] = ChatFireworks()
      
   return models
     
SUPPORTED_MODELS = get_supported_models()
DEFAULT_MODEL = 'gpt-3.5-turbo' # Can  hard code for now to keep simple


CHUNK_SIZES = {  # in tokens, defaults to int(4_096 * 0.8). Override here.
    "gpt-4-0125-preview": int(128_000 * 0.8),
}

ModelNameLiteral = Literal[
    "gpt-3.5-turbo",
    "gpt-4-0125-preview",
    "fireworks",
    "together-ai-mistral-8x7b-instruct-v0.1",
]


def get_chunk_size(model_name: ModelNameLiteral) -> int:
    """Get the chunk size."""
    return CHUNK_SIZES.get(model_name, int(4_096 * 0.8))


def get_model(model_name: Optional[ModelNameLiteral] = None) -> BaseChatModel:
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
