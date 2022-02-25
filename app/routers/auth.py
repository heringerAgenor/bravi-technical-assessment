from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies.models import RegisterKey
from db.db_main import Client
import secrets

router = APIRouter()

@router.post('/auth/key', tags = ["Auth"])
def generate_key(client_form: RegisterKey):
    """
    ## Generates a random shortUUID to serve as API Key.
    """

    flag = True
    client_form = client_form.dict()
    api_key = secrets.token_urlsafe(30)
    client_form["api_key"] = api_key
    flag = Client.add_client(client_form)
    
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {"api_key": api_key},
            "message": "Welcome to Chess Board Storage. The Api Key grants access to your chess board, therefore, keep it safe.",
            "error": None,
        })
    return JSONResponse(content={
        "status": "error",
        "data": {},
        "message": "Generic error!",
        "error": "generic_error",
    }, status_code=400)
