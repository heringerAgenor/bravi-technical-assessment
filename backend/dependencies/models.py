from pydantic import BaseModel, StrictStr, EmailStr


class RegisterForm(BaseModel):
    username       : StrictStr


class AddPieceForm(BaseModel):
    pass
 