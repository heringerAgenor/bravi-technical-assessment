from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies.middleware import check_authentication_header
from dependencies.knight_handler import knight_handler
from dependencies.models import AddPiece, PlacePiece
from db.db_main import Board
import traceback
import shortuuid
import copy

router = APIRouter()


@router.get('/board/pieces', tags=["Board"])
def get_pieces(user = Depends(check_authentication_header)):
    flag = True
    try:
        board = Board.objects(client = user["api_key"]).first()
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


@router.get('/board/piece', tags= ["Board"])
def get_piece(piece_id: str, user = Depends(check_authentication_header)):
    flag = True
    try:
        piece = Board.get_piece(user["api_key"], piece_id)
    except:
        flag = False
        print("Error during board check!")
        print(traceback.format_exc())
    
    if flag:
        if piece:
            return JSONResponse(content={
                "status": "ok",
                "data": {"piece": piece[0][1]},
                "message": "",
                "error": None,
            }, status_code= 200)
        
        return JSONResponse(content={
            "status": "ok",
            "data": {},
            "message": "No piece was found!",
            "error": None,
        }, status_code= 404)

    return JSONResponse(content={
            "status": "error",
            "data": {},
            "message": "Generic error!",
            "error": "generic_error",
        }, status_code=500)


@router.post('/board/add_piece', tags=["Board"])
def add_piece(piece: AddPiece, user = Depends(check_authentication_header)):
    piece = piece.dict()
    piece_id = shortuuid.uuid()
    piece["position"] = ""
    piece["piece_id"] = piece_id

    flag = Board.append_piece(api_key= user["api_key"], new_piece= piece)
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {"piece_id": piece_id},
            "message": "Piece registered successfully!",
            "error": None,
        }, status_code= 404)

    return JSONResponse(content={
            "status": "error",
            "data": {},
            "message": "Generic error!",
            "error": "generic_error",
        }, status_code=500)


@router.put('/board/move_piece', tags=["Board"])
def move_piece(piece_coordinate: PlacePiece, user = Depends(check_authentication_header)):
    # TODO implment error handling here
    
    piece_coordinate = piece_coordinate.dict()
    piece = Board.get_piece(api_key = user["api_key"], piece_id = piece_coordinate["piece_id"])
    piece = copy.deepcopy(piece)   # I was getting some issues with memory reference and the garbage collector but creating a deepcopy solves my problem
    if piece:
        response_data = {}
        piece[0][1]["position"] = f'{piece_coordinate["coordinate"][0]}{piece_coordinate["coordinate"][1]}'
        Board.update_piece(user["api_key"], piece[0][0], piece[0][1])
        if piece[0][1]["type"] == "K":
            response_data["knight_predictions"] = knight_handler.predict_knight_positions(row=piece_coordinate["coordinate"][1], column=piece_coordinate["coordinate"][0])
        return JSONResponse(content={
            "status": "ok",
            "data": response_data,
            "message": "Piece moved successfully!",
            "error": None,
        }, status_code= 200)
    
    return JSONResponse(content={
            "status": "ok",
            "data": {},
            "message": "No piece was found!",
            "error": None,
        }, status_code= 200)


@router.delete('/board/remove_piece', tags=['Board'])
def remove_piece(piece_id: str, user = Depends(check_authentication_header)):
    flag = True
    try:
        Board.remove_piece(user["api_key"], piece_id)
    except:
        flag = False
        print(traceback.format_exc())
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {},
            "message": "Piece deleted successfully!",
            "error": None,
        }, status_code= 200)

    return JSONResponse(content={
            "status": "error",
            "data": {},
            "message": "No piece was found!",
            "error": "Generic error. Try again later!",
        }, status_code= 500)
 