from fastapi import APIRouter, Depends
from dependencies.middleware import manager

router = APIRouter()

@router.get('/board', tags=["Board"])
def board_screen(user = Depends(manager)):
    print(user)