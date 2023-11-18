import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from services.create_router import create_routes


app = FastAPI(
    title="Tinder app for pairs",
    version="0.0.1",
)

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Catch error with valid shemas
    """
    error_messages = []
    for error in exc.errors():
        error_messages.append({"loc": error["loc"], "msg": error["msg"]})
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": error_messages},
    )


app.include_router(create_routes())


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8888, reload=True)
