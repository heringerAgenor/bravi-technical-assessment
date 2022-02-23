from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from dependencies.middleware import NotAuthenticatedException
from routers import (register, login, board)

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(board.router)


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse("/login", status_code=303)


