# Chess Board Storage API

Chess Board Storage API lets you store a whole Chess Board using a strong api key security based model.

# Installation
This project was built using [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) in a linux system. Therefore, the recommended way of installation depends those tools. 
If you're in Windows, use [Docker Desktop](https://docs.docker.com/desktop/windows/install/).

First of all, clone or download the repository. After that, open a shell in the **/app** folder inside the project.
```console
foo@bar:~$ cd {your_awesome_directory}/bravi-technical-assessment/app
```
With the shell opened in the root directory(app folder), run the docker-compose command.
```console
docker-compose up -d --build
```
**And that's it. Now your app is running on localhost in 8000 port.**

# Usage
After installed with docker-compose, a [interactive documentation is available](http://localhost:8000/docs) for testing and read the endpoints. If you don't wanna make HTTP calls with curl ou wget to interact with the API, you shoud use the GUI Docs.

## Authentication
To communicate with the api, **you must generate an API key** and put in headers a field **X-API-Key**. If you don't do that, you'll get a 401, which means that there is no API Key in headers or key is invalid.
  
 You can generate an API key reaching the endpoint by providing a valid username.
 
 `POST /auth/key`
 
 ### Request
 ```console
curl -i -H "Content-Type: application/json"  --request POST --data '{"username": "john_doe"}' http://localhost:8000/auth/key
 ```
### Response
```console
HTTP/1.1 200 OK
date: Fri, 25 Feb 2022 18:41:05 GMT
server: uvicorn
content-length: 206
content-type: application/json

{"status":"ok","data":{"api_key":"36aQ_2U8dO2CUAdqrqkIJN3PXyu2KB-vGK7sgw73"},"message":"Welcome to Chess Board Storage. The Api Key grants access to your chess board, therefore, keep it safe.","error":null
```
Grab your key and keep it safe, you'll need it.

## Interacting with the Board

Now you're ready to go. There are CRUD operations available to store, read, update and delete your pieces on the board. Available endpoints:

- Adding a piece

You can adding a piece by proving the **type** in algebraic notation and **color** of the piece in body parameters:

`POST /board/add_piece`

 ### Request
 ```console
curl -X 'POST' \
  'http://localhost:8000/board/add_piece' \
  -H 'accept: application/json' \
  -H 'X-API-Key: {your_api_key}' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "K",
  "color": "white"
}'
 ```
 ### Response
 ```console
access-control-allow-origin: * 
content-length: 116 
content-type: application/json 
date: Fri,25 Feb 2022 22:03:29 GMT 
server: uvicorn 

{
  "status": "ok",
  "data": {
    "piece_id": "4SbyPwE9sDYHEpss2DrEWB"
  },
  "message": "Piece registered successfully!",
  "error": null
}
 ```
 As you can see, it returns a piece ID. Use it to fetch informations about a specific piece.
 
 - Get a piece
 
 You can fetch a specific piece stored in the API by providing the **piece_id** as query string parameter.
 
 `GET /board/get_piece`
 
 ### Request
 ```console
curl -X 'GET' \
  'http://localhost:8000/board/piece?piece_id={piece_id_here}' \
  -H 'accept: application/json' \
  -H 'X-API-Key: {your_api_key_here}'
 ```
 ### Response
 ```console
 content-length: 137 
 content-type: application/json 
 date: Fri,25 Feb 2022 21:59:01 GMT 
 server: uvicorn 

{
  "status": "ok",
  "data": {
    "piece": {
      "type": "K",
      "color": "white",
      "position": "",
      "piece_id": "dbata2cqGrNLQ6eizSdPiX"
    }
  },
  "message": "",
  "error": null
}
 ````
 
- Get all pieces

You can get all pieces in one request if you want.
 
`GET /board/get_pieces`

### Request
```console
curl -X 'GET' \
  'http://localhost:8000/board/pieces' \
  -H 'accept: application/json' \
  -H 'X-API-Key: {your_api_key_here}'
```
### Response
```console 
content-length: 219 
content-type: application/json 
date: Fri,25 Feb 2022 22:07:08 GMT 
server: uvicorn 

{
  "status": "ok",
  "data": {
    "pieces": [
      {
        "type": "K",
        "color": "white",
        "position": "",
        "piece_id": "dbata2cqGrNLQ6eizSdPiX"
      },
      {
        "type": "K",
        "color": "white",
        "position": "",
        "piece_id": "4SbyPwE9sDYHEpss2DrEWB"
      }
    ]
  },
  "message": "",
  "error": null
}
```

- Move a piece

Here you can change the position of a piece by giving an appropriate cell coordiante in algebraic notation. As an example, a K in e4 position.
If you move a Knight piece (N), you'll get all possibles moves in two turns.

`POST /board/move_piece`

### Request
```console
curl -X 'PUT' \
  'http://localhost:8000/board/move_piece' \
  -H 'accept: application/json' \
  -H 'X-API-Key: {your_api_key_here}' \
  -H 'Content-Type: application/json' \
  -d '{
  "piece_id": "oH4UgLRzCtBajBEFVjRcWo",
  "coordinate": "a1"
}'
```

### Response 
```console
{
  "status": "ok",
  "data": {
    "knight_predictions": {
      "first_turn": [
        "b3",
        "c2"
      ],
      "second_turn": [
        {
          "b3": [
            "a1",
            "c1",
            "a5",
            "c5",
            "d2",
            "d4"
          ]
        },
        {
          "c2": [
            "b4",
            "d4",
            "a1",
            "e1",
            "a3",
            "e3"
          ]
        }
      ]
    }
  },
  "message": "Piece moved successfully!",
  "error": null
}
```

- Remove a piece

Remove a piece from the chess board by providing the piece_id as a query string.

`DELETE /board/remove_piece`

### Request
```console
curl -X 'DELETE' \
  'http://localhost:8000/board/remove_piece?piece_id=dbata2cqGrNLQ6eizSdPiX' \
  -H 'accept: application/json' \
  -H 'X-API-Key: {your_api_key_here}'
```

### Response
```console
access-control-allow-origin: * 
content-length: 78 
content-type: application/json 
date: Fri,25 Feb 2022 22:24:24 GMT 
server: uvicorn 

{
  "status": "ok",
  "data": {},
  "message": "Piece deleted successfully!",
  "error": null
}
```
