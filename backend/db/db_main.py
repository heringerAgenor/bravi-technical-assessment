from typing import List
from mongoengine import *
from mongoengine.connection import connect, disconnect
from mongoengine.document import Document
from mongoengine.fields import (StringField, DictField)
import traceback
import secrets

connect(db = 'bravi_chess_project', host='localhost', alias='bravi_chess_project') 

class Client(Document):
    api_key         = StringField(required = True, primary_key = True)
    username        = StringField(required = True)
    board           = ReferenceField('Board')
    meta            = {"collection": "clients", "db_alias": "bravi_chess_project"}

    @classmethod
    def add_client(cls, user_informations: dict):
        flag = True
        try:
            user_instance = cls(**user_informations)
            user_instance.save()
            user_instance.reload()

            board_instance = Board(pieces = {})
            board_instance.save()
            board_instance.client = user_instance.to_dbref()
            board_instance.save()

            return flag
        except:
            flag =  False
            print("Erro during user creation!")
            print(traceback.format_exc())

        return flag

    @classmethod
    def get_clients(cls, filter_methods: dict = {}) -> List[dict]:
        return [user.to_mongo().to_dict() for user in cls.objects(**filter_methods)]



class Board(Document):
    pieces          = DictField()
    client          = ReferenceField('Client')

    meta            = {"collection": "boards", "db_alias": "bravi_chess_project"}



