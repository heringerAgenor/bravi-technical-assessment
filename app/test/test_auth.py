from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_successfully_registerd():
    response = client.post('/auth/key', json={"username": "john_doe"})
    
    json_response = response.json()
    
    assert response.status_code == 200
    assert json_response["status"] == "ok"
    assert len(json_response["data"]["api_key"]) == 40


def test_username_length():
    response = client.post('/auth/key', json={"username": "john__doe__dev"})
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Username length must be more or qual to 2 and less than or equal to 10."


def test_username_cannot_contain_whitespaces():
    response = client.post('/auth/key', json={"username": "John Doe"})
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Username cannot contain whitespaces."


