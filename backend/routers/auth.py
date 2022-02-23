from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies.models import RegisterForm
from db.db_main import Client
import secrets

router = APIRouter()

@router.post('/auth/key', tags = ["Auth"])
def register_usuer(client_form: RegisterForm):
    flag = True
    client_form = client_form.dict()
    api_key = secrets.token_urlsafe(30)
    client_form["api_key"] = api_key
    flag = Client.add_client(client_form)
    
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {"api_key": api_key},
            "message": "Successfully Registered!",
            "error": None,
        })
    return JSONResponse(content={
        "status": "error",
        "data": {},
        "message": "Generic error!",
        "error": "generic_error",
    }, status_code=400)

# TODO generate new api key and delete