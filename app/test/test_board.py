import json
from fastapi.testclient import TestClient

import sys
sys.path.append('/home/agenor01/Projetcs/bravi-technical-assessment/app')


from main import app

client = TestClient(app)

random_api_key = "NwmtAd0fzlrOov-iO5KDu83ESpW-q9rX2_sTA_aT"
random_piece_id = "Urnfh7PoLBeRawfbGzr3hb"
random_knight_piece_id = "etANrs9KL6jwyvBX7wzYMr"

# get_pieces
def test_pieces_must_return_list():
    response = client.get('/board/pieces', headers={"X-API-Key": random_api_key})
    
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert type(json_response["data"]["pieces"]) == list

# add_piece

def test_add_piece_must_return_piece_id():
    response = client.post('/board/add_piece', json={"type": "K", "color": "black"},headers={"X-API-Key": random_api_key})
    json_response = response.json()
   
    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert "piece_id" in json_response["data"]


def test_add_piece_with_invalid_notation():
    response = client.post('/board/add_piece', json={"type": "a", "color": "black"},headers={"X-API-Key": random_api_key})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "A piece must be a valid chess piece and in algebraic notation."



def test_add_piece_with_wrong_color():
    response = client.post('/board/add_piece', json={"type": "Q", "color": "blue"},headers={"X-API-Key": random_api_key})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Color must be black or white only."

# move_piece


def test_move_piece_successfully():
    response = client.put('/board/move_piece', json={"piece_id": random_piece_id, "coordinate": "c1"}, headers={"X-API-Key": random_api_key})
    
    json_response = response.json()
    
    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert json_response["message"] == "Piece moved successfully!"
    assert json_response["data"] == {}


def test_move_piece_knight_successfully():
    response = client.put('/board/move_piece', json={"piece_id": random_knight_piece_id, "coordinate": "d4"}, headers={"X-API-Key": random_api_key})
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert json_response["message"] == "Piece moved successfully!"
    assert "knight_predictions" in  json_response["data"]


def test_move_piece_with_invalid_piece_id():
    response = client.put('/board/move_piece', json={"piece_id": "i27dbgJ8djgLY2v99Fv5Ro", "coordinate": "d4"}, headers={"X-API-Key": random_api_key})
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["status"] == "error"
    assert json_response["message"] == "No piece was found!"


def test_move_piece_with_invalid_coordinate_length():
    response = client.put('/board/move_piece', json={"piece_id": random_piece_id, "coordinate": "c10"}, headers={"X-API-Key": random_api_key})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Coordinate length must be equal to 2."


def test_move_piece_with_piece_id_length():
    response = client.put('/board/move_piece', json={"piece_id": "asdasdasdsaa", "coordinate": "c10"}, headers={"X-API-Key": random_api_key})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Piece ID length must be equal to 22."


def test_move_piece_with_invalid_column():
    response = client.put('/board/move_piece', json={"piece_id": random_piece_id, "coordinate": "k2"}, headers={"X-API-Key": random_api_key})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Coordinate must have a valid chess Column."


def test_move_piece_with_non_numeric_row():
    response = client.put('/board/move_piece', json={"piece_id": random_piece_id, "coordinate": "cb"}, headers={"X-API-Key": random_api_key})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Coordinate must have valid row number."


def test_move_piece_with_invalid_row():
    response = client.put('/board/move_piece', json={"piece_id": random_piece_id, "coordinate": "c9"}, headers={"X-API-Key": random_api_key})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Coordinate row must be less or equal to 8."


# Remove Piece

def test_remove_piece_successfully():
    response = client.delete(f'/board/remove_piece?piece_id={random_piece_id}', headers={"X-API-Key": random_api_key})

    json_response = response.json()

    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert json_response["message"] == "Piece deleted successfully!"

