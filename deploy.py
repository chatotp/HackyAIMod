import json
import numpy as np

from keras.preprocessing.text import tokenizer_from_json
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import torch

from utils import *
import download

MAX_LEN = 220
MAX_FEATURES = 327009
NUM_AUX = 6

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths
colab_path = "/content/"
kaggle_path = "/kaggle/working/"

prepend_path = "./models/"
if Path(colab_path).exists():
    prepend_path = colab_path
elif Path(kaggle_path).exists():
    prepend_path = kaggle_path

model_path = prepend_path + "model.pth"
embedding_matrix_path = prepend_path + "embeddings.npy"
tokenizer_path = prepend_path + "tokenizer.json"

if not Path.exists(prepend_path):
    download.main()
else:
    print("Models already exist.")

# Load model and params
embedding_matrix = np.load(embedding_matrix_path)
print("Built embedding matrix")

with open(tokenizer_path) as tknzr:
    tokenizer_json = json.load(tknzr)
    tokenizer = tokenizer_from_json(tokenizer_json)
print("Built tokenizer")

model = NeuralNet(embedding_matrix, num_aux_targets=NUM_AUX, max_features=MAX_FEATURES)
model.load_state_dict(torch.load(model_path, map_location=device)['model_state_dict'])
print("Built model")

# Set up FastAPI
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

app = FastAPI()
manager = ConnectionManager()

@app.get("/status", summary="Get status of Application")
async def health():
    return {"status": "healthy"}

@app.get("/receive", summary="Endpoint to receive request from client")
async def receive_request(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote {data}", websocket)
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client has left the chat.")