from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies.models import RegisterForm
from db.db_main import User

router = APIRouter()

@router.post('/register', tags = ["Auth", "Register"])
def register_usuer(user_form: RegisterForm):
    flag = True
    user_form = user_form.dict()
    if User.objects(email = user_form["email"]).first(): 
        return JSONResponse({
            "status": "error",
            "data": {},
            "message": "Email adress is already registered!",
            "error": "register.user_exist"

        })
    flag = User.add_user(user_form)
    if flag:
        return JSONResponse(content={
            "status": "ok",
            "data": {},
            "message": "Successfully Registered!",
            "error": None,
        })
    return JSONResponse(content={
        "status": "error",
        "data": {},
        "message": "Generic error!",
        "error": "generic_error",
    })