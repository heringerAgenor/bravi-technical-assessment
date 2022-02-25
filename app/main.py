from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from routers import (auth, board)

description =  """
Chess Board Storage API lets you store a whole chessboard using strong api key security based model.

## Auth

You can generate your security **key**.
Available functions/routes: 
* **Generate Key** 

## Board
Here you can communicate with the server to manage your pieces in the chessboard.
Available functions/routes: 
* **Add Piece** 
* **Get Piece** 
* **Get Pieces** 
* **Move Piece** 
* **Delete Piece** 



Developed by [Agenor Heringer](https://github.com/heringerAgenor)
"""


tags_metadata = [
    {
        "name": "Auth",
        "description": "Security handler. API Key generation goes here.",
    },
    {
        "name": "Board",
        "description": "Manage chess board pieces. Scope crud operations and some aditional features.",
    },
]

app = FastAPI(
    title="Chess Board Storage API", 
    docs_url='/docs',
    version="0.0.1",
    description = description,
    openapi_tags=tags_metadata,
    redoc_url=None
    
    )

app.include_router(auth.router)
app.include_router(board.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


