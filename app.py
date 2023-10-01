import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Tinder app for pairs",
    version="0.0.1",
)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
