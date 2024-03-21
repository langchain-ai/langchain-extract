🚧 Under Active Development 🚧

This repo is under active developments. Do not use code from `main`. Instead please checkout code from [releases](https://github.com/langchain-ai/langchain-extract/releases)

This repository is not a library, but a jumping point for your own application -- so do not be surprised to find breaking changes between releases!

# 🦜⛏️ LangChain Extract

[![CI](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/langchain-ai/langchain-extract/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchainai.svg?style=social&label=Follow%20%40LangChainAI)](https://twitter.com/langchainai)
[![](https://dcbadge.vercel.app/api/server/6adMQxSpJS?compact=true&style=flat)](https://discord.gg/6adMQxSpJS)
[![Open Issues](https://img.shields.io/github/issues-raw/langchain-ai/langchain-extract)](https://github.com/langchain-ai/langchain-extract/issues)

`langchain-extract` is a simple web server that allows you to extract information from text and files using LLMs. It is build using [FastAPI](https://fastapi.tiangolo.com/), [LangChain](https://python.langchain.com/) and [Postgresql](https://www.postgresql.org/).

The backend closely follows the [extraction use-case documentation](https://python.langchain.com/docs/use_cases/extraction) and provides
a reference implementation of an app that helps to do extraction over data using LLMs.

This repository is meant to be a starting point for building your own extraction application which
may have slightly different requirements or use cases.

## Functionality 

- 🚀 FastAPI webserver with a REST API
- 📚 OpenAPI Documentation
- 📝 Use [JSON Schema](https://json-schema.org/) to define what to extract
- 📊 Use examples to improve the quality of extracted results
- 📦 Create and save extractors and examples in a database
- 📂 Extract information from text and/or binary files
- 🦜️🏓 [LangServe](https://github.com/langchain-ai/langserve) endpoint to integrate with LangChain `RemoteRunnnable`

## Releases:

0.0.1: https://github.com/langchain-ai/langchain-extract/releases/tag/0.0.1

## 📚 Documentation

See the example notebooks in the [documentation](https://github.com/langchain-ai/langchain-extract/tree/main/docs/source/notebooks)
to see how to create examples to improve extraction results, upload files (e.g., HTML, PDF) and more.

Documentation and server code are both under development!

## 🍯 Example API

Below are two sample `curl` requests to demonstrate how to use the API.

These only provide minimal examples of how to use the API, 
see the [documentation](https://github.com/langchain-ai/langchain-extract/tree/main/docs/source/notebooks) for more information
about the API and the [extraction use-case documentation](https://python.langchain.com/docs/use_cases/extraction) for more information about how to extract
information using LangChain.

First we generate a user ID for ourselves. The application does not manage users or authentication. Access to extractors, few-shot examples, and other artifacts is controlled via this ID, which is managed via cookies in the front end. Consider it secret.
```sh
USER_ID=$(uuidgen)
export USER_ID
```

### Create an extractor

```sh
curl -X 'POST' \
  'http://localhost:8000/extractors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  --cookie "user_id=${USER_ID}" \
  -d '{
  "name": "Personal Information",
  "description": "Use to extract personal information",
  "schema": {
      "type": "object",
      "title": "Person",
      "required": [
        "name",
        "age"
      ],
      "properties": {
        "age": {
          "type": "integer",
          "title": "Age"
        },
        "name": {
          "type": "string",
          "title": "Name"
        }
      }
    },
  "instruction": "Use information about the person from the given user input."
}'
```

Response:

```json
{
  "uuid": "e07f389f-3577-4e94-bd88-6b201d1b10b9"
}
```

Use the extract endpoint to extract information from the text (or a file)
using an existing pre-defined extractor.

```sh
curl -s -X 'POST' \
'http://localhost:8000/extract' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
--cookie "user_id=${USER_ID}" \
-F 'extractor_id=e07f389f-3577-4e94-bd88-6b201d1b10b9' \
-F 'text=my name is chester and i am 20 years old. My name is eugene and I am 1 year older than chester.' \
-F 'mode=entire_document' \
-F 'file=' | jq .
```

Response:

```json
{
  "data": [
    {
      "name": "chester",
      "age": 20
    },
    {
      "name": "eugene",
      "age": 21
    }
  ]
}
```

Add a few shot example:
```sh
curl -X POST "http://localhost:8000/examples" \
    -H "Content-Type: application/json" \
    --cookie "user_id=${USER_ID}" \
    -d '{
          "extractor_id": "e07f389f-3577-4e94-bd88-6b201d1b10b9",
          "content": "marcos is 10.",
          "output": [
            {
              "name": "MARCOS",
              "age": 10
            }
          ]
        }' | jq .
```
The response will contain a UUID for the example. Examples can be deleted with a DELETE request. This example is now persisted and associated with our extractor, and subsequent extraction runs will incorporate it.

## ✅ Running locally

The easiest way to get started is to use `docker-compose` to run the server.

**Configure the environment**

Add `.local.env` file to the root directory with the following content:

```sh
OPENAI_API_KEY=... # Your OpenAI API key
```

Adding `FIREWORKS_API_KEY` or `TOGETHER_API_KEY` to this file would enable additional models. You can access available models for the server and other information via a `GET` request to the `configuration` endpoint.

Build the images:
```sh
docker compose build
```

Run the services:

```sh
docker compose up
```

This will launch both the extraction server and the postgres instance.

Verify that the server is running:

```sh
curl -X 'GET' 'http://localhost:8000/ready'
```

This should return `ok`.

## Contributions

Feel free to develop in this project for your own needs!
For now, we are not accepting pull requests, but would love to hear [questions, ideas or issues](https://github.com/langchain-ai/langchain-extract/discussions).

## Development

To set up for development, you will need to install [Poetry](https://python-poetry.org/).

The backend code is located in the `backend` directory.

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

### Linting and format

Testing and formatting is done using a Makefile inside `[root]/backend`

```sh
make format
```
