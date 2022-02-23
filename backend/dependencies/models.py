from pydantic import BaseModel, StrictStr, StrictInt, EmailStr


class LoginForm(BaseModel):
    email       : EmailStr
    password    : StrictStr

    
class RegisterForm(BaseModel):
    email       : EmailStr
    username    : StrictStr
    password    : StrictStr 