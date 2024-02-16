"""Entry point into the app"""
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
