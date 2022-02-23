from db.db_main import User
from fastapi_login import LoginManager

# Secret generated using -> import os; print(os.urandom(24).hex()
SECRET = 'c5f56dd8d21ce8df693bc77787db133301e6c89067b8b14d'

manager = LoginManager(SECRET, '/login', use_cookie=True)
manager.cookie_name = "bravi_chess"

class NotAuthenticatedException(Exception):
    pass

manager.not_authenticated_exception = NotAuthenticatedException

@manager.user_loader
async def load_user(email: str):
    """
        Procura o usuario do banco e retorna as informações se o encontrar
    """
    try:
        return User.objects(email = email).first()
    except Exception as e:
        print('Erro ao buscar dados no middleware')