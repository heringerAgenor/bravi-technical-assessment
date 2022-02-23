from typing import List
from mongoengine import *
from mongoengine.connection import connect, disconnect
from mongoengine.document import Document
from mongoengine.fields import (StringField, EmailField, ListField)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
connect(db = 'bravi_chess_project', host='localhost', alias='bravi_chess_project') 

class User(Document):
    email           = EmailField()
    username        = StringField(required=True)
    password        = StringField(required=True)
    board           = ReferenceField('Board')
    meta            = {"collection": "users", "db_alias": "bravi_chess_project"}

    @classmethod
    def add_user(cls, user_informations: dict):
        try:
            user_informations['password'] = pwd_context.hash(user_informations['password'])
            user_instance = cls(**user_informations)
            user_instance.validate()
            user_instance.save()
            user_instance.reload()
            return True
        except Exception:
            return False

    @classmethod
    def get_user(cls, filter_methods: dict = {}) -> List:
        return [user.to_mongo().to_dict() for user in cls.objects(**filter_methods)]


    def verify_password(self, passwrod: str):
        return pwd_context.verify(passwrod, self.password)

class Board(Document):
    board = ListField(ListField(StringField))
    user  = ReferenceField('User')




