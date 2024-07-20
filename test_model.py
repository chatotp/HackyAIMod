import json
import numpy as np

from keras.preprocessing.text import tokenizer_from_json
from pathlib import Path
import torch

from utils import *

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

# Load model and params
embedding_matrix = np.load(embedding_matrix_path)

with open(tokenizer_path) as tknzr:
    tokenizer_json = json.load(tknzr)
    tokenizer = tokenizer_from_json(tokenizer_json)

model = NeuralNet(embedding_matrix, num_aux_targets=NUM_AUX, max_features=MAX_FEATURES)
model.load_state_dict(torch.load(model_path, map_location=device)['model_state_dict'])

test_text = "This is a test text."
prediction = predict(test_text, model, tokenizer, device)
print(f'Prediction: {"Toxic" if prediction[0][0] > 0.5 else "Not Toxic"}')

test_text = "Shit! This is bad."
prediction = predict(test_text, model, tokenizer, device)
print(f'Prediction: {"Toxic" if prediction[0][0] > 0.5 else "Not Toxic"}')