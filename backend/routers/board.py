from http import client
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies.middleware import check_authentication_header
from dependencies.board_handler import board_handler
from db.db_main import Board
import traceback

router = APIRouter()


@router.get('/pieces', tags=["Board"])
def get_pieces(user = Depends(check_authentication_header)):
    flag = True
    try:
        board = Board.objects(client = user["api_key"]).first()
        print(board)
    except:
        flag = False
        print("Error during board check!")
        print(traceback.format_exc())
    
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {"pieces": board.pieces},
            "message": "",
            "error": None,
        }, status_code= 200)

    return JSONResponse(content={
            "status": "error",
            "data": {},
            "message": "Generic error!",
            "error": "generic_error",
        }, status_code=400)


@router.post('/add_piece', tags=["Board"])
def add_piece(user = Depends(check_authentication_header)):
    flag = True
    try:
        board = Board.objects(user = user.id).first()

    except:
        flag = False
        print()

