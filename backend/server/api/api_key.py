from fastapi.security import APIKeyHeader

# For actual auth, you'd need to check the key against a database or some other
# data store. Here, we don't need actual auth, just a key that matches
# a UUID
UserToken = APIKeyHeader(name="x-key")
