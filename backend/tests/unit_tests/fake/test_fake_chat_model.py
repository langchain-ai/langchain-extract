"""Tests for verifying that testing utility code works as expected."""
from itertools import cycle

from langchain_core.messages import AIMessage

from tests.unit_tests.fake.chat_model import GenericFakeChatModel


class AnyStr(str):
    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, str)


def test_generic_fake_chat_model_invoke() -> None:
    # Will alternate between responding with hello and goodbye
    infinite_cycle = cycle([AIMessage(content="hello"), AIMessage(content="goodbye")])
    model = GenericFakeChatModel(messages=infinite_cycle)
    response = model.invoke("meow")
    assert response == AIMessage(content="hello", id=AnyStr())
    response = model.invoke("kitty")
    assert response == AIMessage(content="goodbye", id=AnyStr())
    response = model.invoke("meow")
    assert response == AIMessage(content="hello", id=AnyStr())


async def test_generic_fake_chat_model_ainvoke() -> None:
    # Will alternate between responding with hello and goodbye
    infinite_cycle = cycle([AIMessage(content="hello"), AIMessage(content="goodbye")])
    model = GenericFakeChatModel(messages=infinite_cycle)
    response = await model.ainvoke("meow")
    assert response == AIMessage(content="hello", id=AnyStr())
    response = await model.ainvoke("kitty")
    assert response == AIMessage(content="goodbye", id=AnyStr())
    response = await model.ainvoke("meow")
    assert response == AIMessage(content="hello", id=AnyStr())
