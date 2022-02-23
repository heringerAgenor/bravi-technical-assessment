from fastapi import FastAPI, Request
from routers import (auth, board)


app = FastAPI()

app.include_router(auth.router)
app.include_router(board.router)

