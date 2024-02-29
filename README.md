🚧 Under Active Development 🚧

Please expect breaking changes!

# 🦜⛏️ LangChain Extract

[![CI](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchainai.svg?style=social&label=Follow%20%40LangChainAI)](https://twitter.com/langchainai)
[![](https://dcbadge.vercel.app/api/server/6adMQxSpJS?compact=true&style=flat)](https://discord.gg/6adMQxSpJS)
[![Open Issues](https://img.shields.io/github/issues-raw/langchain-ai/langchain-extract)](https://github.com/langchain-ai/langchain-extract/issues)

This repo is an implementation of a locally hosted extraction service.

It's build with LangChain, FastAPI and Postgresql.

## ✅ Running locally

The `backend` code is located in `/backend`. 

The backend code relies on having access to a postgres instance. 


### Launch Postgres

Use the `docker-compose.yml` file in the root directory to launch a postgres instance.

```sh
docker compose up postgres
```

### Launch the extraction webserver

At the moment, we don't have the backend defined in docker compose, so
you'll need to set up the backend.

```sh
cd backend
```

Set up the environment using poetry:

```sh
poetry install --with lint,dev,test
```

Run the following script to create a database and schema:

```sh
python -m scripts.run_migrations create 
```

From `/backend`:

```sh
OPENAI_API_KEY=[YOUR API KEY] python -m server.main
```

## Set up for development

Use this if you want to develop in your own fork of the repo.

For now, we will not be accepting pull requests, but would love to hear any feedback
about ideas or issues etc.

### Testing 

Create a test database. The test database is used for running tests and is
separate from the main database. It will have the same schema as the main
database.

```sh
python -m scripts.run_migrations create-test-db
```

Run the tests

```sh
make test
```

# Linting and format

Testing and formatting is done using a Makefile inside `[root]/backend`

```sh
make format
```