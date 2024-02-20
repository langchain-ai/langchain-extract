🚧 Under Active Development 🚧


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
