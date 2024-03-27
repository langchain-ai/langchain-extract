

# Revanguard Document AI

## Functionality 

- 🚀 FastAPI webserver with a REST API
- 📚 OpenAPI Documentation
- 📝 Use [JSON Schema](https://json-schema.org/) to define what to extract
- 📊 Use examples to improve the quality of extracted results
- 📦 Create and save extractors and examples in a database
- 📂 Extract information from text and/or binary files
- 🦜️🏓 [LangServe](https://github.com/langchain-ai/langserve) endpoint to integrate with LangChain `RemoteRunnnable`


## 🍯 Example API

Below are two sample `curl` requests to demonstrate how to use the API.

These only provide minimal examples of how to use the API.

First we generate a user ID for ourselves. **The application does not properly manage users or include legitimate authentication**. Access to extractors, few-shot examples, and other artifacts is controlled via this ID. Consider it secret.
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
  -H "x-key: ${USER_ID}" \
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
-H "x-key: ${USER_ID}" \
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
    -H "x-key: ${USER_ID}" \
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

This will launch the extraction server.

Verify that the server is running:

```sh
curl -X 'GET' 'http://localhost:8000/ready'
```

This should return `ok`.

The UI will be available at [http://localhost:3000](http://localhost:3000).

