"""Fake Chat Model wrapper for testing purposes."""
from typing import Any, Iterator, List, Optional

from langchain_core.callbacks.manager import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult


class GenericFakeChatModel(BaseChatModel):
    """A generic fake chat model that can be used to test the chat model interface."""

    messages: Iterator[AIMessage]
    """Get an iterator over messages.

    This can be expanded to accept other types like Callables / dicts / strings
    to make the interface more generic if needed.

    Note: if you want to pass a list, you can use `iter` to convert it to an iterator.

    Please note that streaming is not implemented yet. We should try to implement it
    in the future by delegating to invoke and then breaking the resulting output
    into message chunks.
    """

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Top Level call"""
        message = next(self.messages)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "generic-fake-chat-model"
