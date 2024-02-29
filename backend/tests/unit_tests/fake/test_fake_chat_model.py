"""Tests for verifying that testing utility code works as expected."""
from itertools import cycle

from langchain_core.messages import AIMessage

from tests.unit_tests.fake.chat_model import GenericFakeChatModel


def test_generic_fake_chat_model_invoke() -> None:
    # Will alternate between responding with hello and goodbye
    infinite_cycle = cycle([AIMessage(content="hello"), AIMessage(content="goodbye")])
    model = GenericFakeChatModel(messages=infinite_cycle)
    response = model.invoke("meow")
    assert response == AIMessage(content="hello")
    response = model.invoke("kitty")
    assert response == AIMessage(content="goodbye")
    response = model.invoke("meow")
    assert response == AIMessage(content="hello")


async def test_generic_fake_chat_model_ainvoke() -> None:
    # Will alternate between responding with hello and goodbye
    infinite_cycle = cycle([AIMessage(content="hello"), AIMessage(content="goodbye")])
    model = GenericFakeChatModel(messages=infinite_cycle)
    response = await model.ainvoke("meow")
    assert response == AIMessage(content="hello")
    response = await model.ainvoke("kitty")
    assert response == AIMessage(content="goodbye")
    response = await model.ainvoke("meow")
    assert response == AIMessage(content="hello")
