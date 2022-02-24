from http import client
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

            board_instance = Board()
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
    pieces          = ListField(DictField())
    client          = ReferenceField('Client')

    meta            = {"collection": "boards", "db_alias": "bravi_chess_project"}


    @classmethod
    def append_piece(cls, api_key: str, new_piece: dict):
        flag = True
        try:
            board = cls.objects(client = api_key).first()
            board.pieces.append(new_piece)
            board.save()
            board.reload()
        except:
            flag = False
            print("Error during apending a new piece!")
            print(traceback.format_exc())
        return flag
    
    @classmethod
    def get_piece(cls, api_key: str, piece_id: str):
        return [(index, value) for index, value in enumerate(cls.objects(client = api_key).first().pieces) if value["piece_id"] == piece_id]

    @classmethod
    def update_piece(cls, api_key: str, piece_index_position: int, new_content: dict ):
        return cls.objects(client = api_key).update(__raw__ = {"$set": {f"pieces.{piece_index_position}": new_content}})

        #f"pieces.{piece_index_position}"