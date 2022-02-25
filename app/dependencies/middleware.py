from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
from db.db_main import Client



def check_authentication_header(x_api_key: str = Depends(APIKeyHeader(name='X-API-Key'))):
    client = Client.objects(api_key = x_api_key).first()
    if client:
        return {"api_key": x_api_key, "username": client.username}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )