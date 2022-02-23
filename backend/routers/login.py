from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dependencies.models import LoginForm
from dependencies.middleware import load_user, manager, SECRET
from datetime import timedelta, datetime
import jwt


router = APIRouter()


@router.post('/login', tags= ["Auth", "Login"])
async def login_user(login_form: LoginForm,  request: Request):
    login_form  = login_form.dict()
    user = await load_user(login_form["email"])
    if not user or not user.verify_password(login_form["password"]):
        return JSONResponse(content={
            "status": "error",
            "data": {},
            "message": "Email or password invalid!",
            "error": "credentials.invalid"
        })

    access_token = manager.create_access_token(
            data={"sub": user.email,  "id": str(user.id)},
            expires=timedelta(hours=6)
        )
    resp = JSONResponse(content={
        "status": "ok",
        "data": {
            "username": user.username,
            "email": user.email,
            "token": jwt.encode({
                "sub":  str(user.id), 
                "exp": datetime.utcnow() + timedelta(hours=6)
            }, SECRET, "HS256"),
            'isLoggedIn': True
        },
        "message": None,
        "error": None
    })

    manager.set_cookie(resp, access_token)

    return resp


@router.delete('/logout', tags= ["Auth", "Login"])
async def logout_user(request: Request):
    resp = JSONResponse(content={
            "status": "ok",
            "data": {},
            "message": None,
            "error": None
        })
    resp.delete_cookie("bravi_chess")
    return resp