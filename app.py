from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from services.create_router import create_routes


app = FastAPI(
    title="Tinder app for pairs",
    version="0.0.1",
)


@app.get("/")
async def temporary_route():
    """
    Temporary view to redirect on docs page
    """
    return RedirectResponse("/docs")


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
