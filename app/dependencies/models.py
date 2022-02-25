from pydantic import BaseModel, StrictStr, validator

valid_pieces       = {"K", "Q", "R", "B", "N", "P"}
valid_columns      = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
class RegisterKey(BaseModel):
    username       : StrictStr

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
            }
        }
class AddPiece(BaseModel):
    type           : StrictStr
    color          : StrictStr

    class Config:
        schema_extra = {
            "example": {
                "type": "K",
                "color": "white"
            }
        }


    @validator('type')
    def type_must_be_valid(cls, v):
        v = v.upper() 
        if v not in valid_pieces:
            raise ValueError("A piece must be a valid chess piece and in algebraic notation.")
        return v
    
    @validator("color")
    def color_must_be_black_or_white(cls, v):
        v = v.lower()
        if v not in {"black", "white"}:
            raise ValueError("Color must be black or white only.")
        return v


class PlacePiece(BaseModel):
    piece_id       : StrictStr
    coordinate     : StrictStr

    class Config:
        schema_extra = {
            "example": {
                "piece_id": "gQPZQC9hEWQubWVUEPNNCA",
                "coordinate": "e4"
            }
        }

    @validator('piece_id')
    def piece_id_length_must_be_twenty_two(cls, v):
        if not len(v) == 22:
            raise ValueError("Piece ID length must be equal to 22.")
        return v
    
    @validator("coordinate")
    def coordiante_must_be_valid(cls, v):

        if not len(v) == 2:
            raise ValueError("Coordinate length must be equal to 2.")
        elif v[0] not in valid_columns:
            raise ValueError("Coordinate must have a valid chess Column.") 
        elif not v[1].isnumeric():
            raise ValueError("Coordinate must have valid row number.")
        elif int(v[1]) > 8:
            raise ValueError("Coordinate row must be less or equal to 8.")
        return (v[0], int(v[1]))