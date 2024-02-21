# 🦜? LangChain Extract

[![CI](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchainai.svg?style=social&label=Follow%20%40LangChainAI)](https://twitter.com/langchainai)
[![](https://dcbadge.vercel.app/api/server/6adMQxSpJS?compact=true&style=flat)](https://discord.gg/6adMQxSpJS)
[![Open Issues](https://img.shields.io/github/issues-raw/langchain-ai/langchain-extract)](https://github.com/langchain-ai/langchain-extract/issues)


# Set up

## Services

The root folder contains a docker compose file which will a launch a postgres
instance.

```
docker compose up
```

At the time of writing, the app wasn't using postgres yet!

## App

```sh
cd [root]/backend
```

Set up the environment using poetry:

```sh
poetry install --with lint,dev,test
```

Verify that unit tests pass (they probably wont?)

# Test and format

Testing and formatting is done using a Makefile inside `[root]/backend`

```sh
make format
```

```sh
make test
```

# Launch Server

From `[root]/backend`:

```sh
python -m server.main
```

# Example client

See `docs/source/notebooks` for an example client.
